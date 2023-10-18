import math
import mmap
import os
import posixpath
import tempfile
import typing
import uuid
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait
from shutil import rmtree
from threading import Event
from typing import Any, Callable, List, NamedTuple, Optional, Tuple

import requests
from mlflow.entities import (
    FileInfo,
    MultiPartUpload,
    MultiPartUploadStorageProvider,
    SignedURL,
)
from mlflow.store.artifact.artifact_repo import ArtifactRepository
from mlflow.tracking import MlflowClient
from mlflow.utils.file_utils import relative_path_to_artifact_path
from mlflow.utils.rest_utils import (
    augmented_raise_for_status,
    cloud_storage_http_request,
)
from tqdm.utils import CallbackIOWrapper

from mlfoundry.env_vars import DISABLE_MULTIPART_UPLOAD
from mlfoundry.exceptions import MlFoundryException
from mlfoundry.logger import logger
from mlfoundry.tracking.entities import ArtifactCredential
from mlfoundry.tracking.truefoundry_rest_store import TruefoundryRestStore

_MIN_BYTES_REQUIRED_FOR_MULTIPART = 100 * 1024 * 1024
_MULTIPART_DISABLED = os.getenv(DISABLE_MULTIPART_UPLOAD, "").lower() == "true"
# GCP/S3 Maximum number of parts per upload	10,000
# Maximum number of blocks in a block blob 50,000 blocks
# TODO: This number is artificially limited now. Later
# we will ask for parts signed URI in batches rather than in a single
# API Calls:
# Create Multipart Upload (Returns maximum number of parts, size limit of
#                            a single part, upload id for s3 etc )
#   Get me signed uris for first 500 parts
#     Upload 500 parts
#   Get me signed uris for the next 500 parts
#     Upload 500 parts
#   ...
# Finalize the Multipart upload using the finalize signed url returned
# by Create Multipart Upload or get a new one.
_MAX_NUM_PARTS_FOR_MULTIPART = 1000
# Azure Maximum size of a block in a block blob	4000 MiB
# GCP/S3 Maximum size of an individual part in a multipart upload 5 GiB
_MAX_PART_SIZE_BYTES_FOR_MULTIPART = 4 * 1024 * 1024 * 1000
_MAX_WORKERS_FOR_UPLOAD = max(min(32, os.cpu_count() * 2), 4)
_MAX_WORKERS_FOR_DOWNLOAD = max(min(32, os.cpu_count() * 2), 4)
_LIST_FILES_PAGE_SIZE = 500
_GENERATE_SIGNED_URL_BATCH_SIZE = 50


def _align_part_size_with_mmap_allocation_granularity(part_size: int) -> int:
    modulo = part_size % mmap.ALLOCATIONGRANULARITY
    if modulo == 0:
        return part_size

    part_size += mmap.ALLOCATIONGRANULARITY - modulo
    return part_size


# Can not be less than 5 * 1024 * 1024
_PART_SIZE_BYTES_FOR_MULTIPART = _align_part_size_with_mmap_allocation_granularity(
    10 * 1024 * 1024
)


class TruefoundryArtifactRepository(ArtifactRepository):
    # TODO (chiragjn): This class needs to be removed, already dependents are deprecated
    def __init__(
        self,
        artifact_uri,
        rest_store: TruefoundryRestStore,
        credentials=None,
        storage_integration_id=None,
    ):
        self.artifact_uri = artifact_uri
        super().__init__(artifact_uri)
        self.rest_store: TruefoundryRestStore = rest_store

    @staticmethod
    def _extract_run_id(artifact_uri) -> str:
        # artifact_uri will be something like,
        # s3://<BUCKET>/<PATH>/<EXP_ID>/<RUN_ID>/artifacts
        run_id = artifact_uri.rstrip("/").split("/")[-2]
        return run_id

    def list_artifacts(self, path=None, **kwargs) -> typing.List[FileInfo]:
        run_id = self._extract_run_id(self.artifact_uri)
        artifacts = self.rest_store.list_artifacts(run_id=run_id, path=path)
        return artifacts

    def _signed_url_upload_file(
        self, artifact_credential: ArtifactCredential, local_file: str
    ):
        if os.stat(local_file).st_size == 0:
            with cloud_storage_http_request(
                "put",
                artifact_credential.signed_uri,
                data="",
            ) as response:
                response.raise_for_status()
        else:
            with open(local_file, "rb") as file:
                with cloud_storage_http_request(
                    "put",
                    artifact_credential.signed_uri,
                    data=file,
                ) as response:
                    response.raise_for_status()

    def log_artifacts(self, local_dir, artifact_path=None):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)
        for (root, _, file_names) in os.walk(local_dir):
            upload_path = dest_path
            if root != local_dir:
                rel_path = os.path.relpath(root, local_dir)
                rel_path = relative_path_to_artifact_path(rel_path)
                upload_path = posixpath.join(dest_path, rel_path)
            for file_name in file_names:
                local_file = os.path.join(root, file_name)
                self.log_artifact(local_file=local_file, artifact_path=upload_path)

    def log_artifact(self, local_file, artifact_path=None):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)
        dest_path = posixpath.join(dest_path, os.path.basename(local_file))
        artifact_credential = self.rest_store.get_artifact_write_credential(
            run_id=self._extract_run_id(self.artifact_uri), path=dest_path
        )
        self._signed_url_upload_file(artifact_credential, local_file)

    def _download_file(self, remote_file_path: str, local_path: str):
        if not remote_file_path:
            raise MlFoundryException(
                f"remote_file_path cannot be None or empty str {remote_file_path}"
            )

        artifact_credential = self.rest_store.get_artifact_read_credentials(
            run_id=self._extract_run_id(self.artifact_uri), path=remote_file_path
        )
        _download_file_using_http_uri(
            http_uri=artifact_credential.signed_uri, download_path=local_path
        )


class _PartNumberEtag(NamedTuple):
    part_number: int
    etag: str


def _get_s3_compatible_completion_body(multi_parts: List[_PartNumberEtag]) -> str:
    body = "<CompleteMultipartUpload>\n"
    for part in multi_parts:
        body += "  <Part>\n"
        body += f"    <PartNumber>{part.part_number}</PartNumber>\n"
        body += f"    <ETag>{part.etag}</ETag>\n"
        body += "  </Part>\n"
    body += "</CompleteMultipartUpload>"
    return body


def _get_azure_blob_completion_body(block_ids: List[str]) -> str:
    body = "<BlockList>\n"
    for block_id in block_ids:
        body += f"<Uncommitted>{block_id}</Uncommitted> "
    body += "</BlockList>"
    return body


class _FileMultiPartInfo(NamedTuple):
    num_parts: int
    part_size: int
    file_size: int


def _decide_file_parts(file_path: str) -> _FileMultiPartInfo:
    file_size = os.path.getsize(file_path)
    if file_size < _MIN_BYTES_REQUIRED_FOR_MULTIPART or _MULTIPART_DISABLED:
        return _FileMultiPartInfo(1, part_size=file_size, file_size=file_size)

    ideal_num_parts = math.ceil(file_size / _PART_SIZE_BYTES_FOR_MULTIPART)
    if ideal_num_parts <= _MAX_NUM_PARTS_FOR_MULTIPART:
        return _FileMultiPartInfo(
            ideal_num_parts,
            part_size=_PART_SIZE_BYTES_FOR_MULTIPART,
            file_size=file_size,
        )

    part_size_when_using_max_parts = math.ceil(file_size / _MAX_NUM_PARTS_FOR_MULTIPART)
    part_size_when_using_max_parts = _align_part_size_with_mmap_allocation_granularity(
        part_size_when_using_max_parts
    )
    if part_size_when_using_max_parts > _MAX_PART_SIZE_BYTES_FOR_MULTIPART:
        raise ValueError(
            f"file {file_path!r} is too big for upload. Multipart chunk"
            f" size {part_size_when_using_max_parts} is higher"
            f" than {_MAX_PART_SIZE_BYTES_FOR_MULTIPART}"
        )
    num_parts = math.ceil(file_size / part_size_when_using_max_parts)
    return _FileMultiPartInfo(
        num_parts, part_size=part_size_when_using_max_parts, file_size=file_size
    )


def _signed_url_upload_file(
    signed_url: SignedURL, local_file: str, abort_event: Optional[Event] = None
):
    if os.stat(local_file).st_size == 0:
        with cloud_storage_http_request("put", signed_url.url, data="") as response:
            response.raise_for_status()
            return

    def callback(*_, **__):
        if abort_event and abort_event.is_set():
            raise Exception("aborting upload")

    with open(local_file, "rb") as file:
        # NOTE: Azure Put Blob does not support Transfer Encoding header.
        wrapped_file = CallbackIOWrapper(callback, file, "read")
        with cloud_storage_http_request(
            "put", signed_url.url, data=wrapped_file
        ) as response:
            response.raise_for_status()


def _download_file_using_http_uri(
    http_uri, download_path, chunk_size=100000000, callback: Callable[[], Any] = None
):
    """
    Downloads a file specified using the `http_uri` to a local `download_path`. This function
    uses a `chunk_size` to ensure an OOM error is not raised a large file is downloaded.
    Note : This function is meant to download files using presigned urls from various cloud
            providers.
    """
    with cloud_storage_http_request("get", http_uri, stream=True) as response:
        augmented_raise_for_status(response)
        with open(download_path, "wb") as output_file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if callback:
                    callback()
                if not chunk:
                    break
                output_file.write(chunk)


class _CallbackIOWrapperForMultiPartUpload(CallbackIOWrapper):
    def __init__(self, callback, stream, method, length: int):
        self.wrapper_setattr("_length", length)
        super().__init__(callback, stream, method)

    def __len__(self):
        return self.wrapper_getattr("_length")


def _file_part_upload(
    url: str,
    file_path: str,
    seek: int,
    length: int,
    file_size: int,
    abort_event: Optional[Event] = None,
    method: str = "put",
):
    def callback(*_, **__):
        if abort_event and abort_event.is_set():
            raise Exception("aborting upload")

    with open(file_path, "rb") as file:
        with mmap.mmap(
            file.fileno(),
            length=min(file_size - seek, length),
            offset=seek,
            access=mmap.ACCESS_READ,
        ) as mapped_file:
            wrapped_file = _CallbackIOWrapperForMultiPartUpload(
                callback, mapped_file, "read", len(mapped_file)
            )
            with cloud_storage_http_request(
                method,
                url,
                data=wrapped_file,
            ) as response:
                response.raise_for_status()
                return response


def _s3_compatible_multipart_upload(
    multipart_upload: MultiPartUpload,
    local_file: str,
    multipart_info: _FileMultiPartInfo,
    executor: ThreadPoolExecutor,
    abort_event: Optional[Event] = None,
):
    abort_event = abort_event or Event()
    parts = []

    def upload(part_number: int, seek: int):
        logger.debug(
            "Uploading part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )
        response = _file_part_upload(
            url=multipart_upload.part_signed_urls[part_number].url,
            file_path=local_file,
            seek=seek,
            length=multipart_info.part_size,
            file_size=multipart_info.file_size,
            abort_event=abort_event,
        )
        logger.debug(
            "Uploaded part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )
        etag = response.headers["ETag"]
        parts.append(_PartNumberEtag(etag=etag, part_number=part_number + 1))

    futures = []
    for part_number, seek in enumerate(
        range(0, multipart_info.file_size, multipart_info.part_size)
    ):
        future = executor.submit(upload, part_number=part_number, seek=seek)
        futures.append(future)

    done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
    if len(not_done) > 0:
        abort_event.set()
    for future in not_done:
        future.cancel()
    for future in done:
        if future.exception() is not None:
            raise future.exception()

    logger.debug("Finalizing multipart upload of %s", local_file)
    parts = sorted(parts, key=lambda part: part.part_number)
    response = requests.post(
        multipart_upload.finalize_signed_url.url,
        data=_get_s3_compatible_completion_body(parts),
        timeout=2 * 60,
    )
    response.raise_for_status()
    logger.debug("Multipart upload of %s completed", local_file)


def _azure_multi_part_upload(
    multipart_upload: MultiPartUpload,
    local_file: str,
    multipart_info: _FileMultiPartInfo,
    executor: ThreadPoolExecutor,
    abort_event: Optional[Event] = None,
):
    abort_event = abort_event or Event()

    def upload(part_number: int, seek: int):
        logger.debug(
            "Uploading part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )
        _file_part_upload(
            url=multipart_upload.part_signed_urls[part_number].url,
            file_path=local_file,
            seek=seek,
            length=multipart_info.part_size,
            file_size=multipart_info.file_size,
            abort_event=abort_event,
        )
        logger.debug(
            "Uploaded part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )

    futures = []
    for part_number, seek in enumerate(
        range(0, multipart_info.file_size, multipart_info.part_size)
    ):
        future = executor.submit(upload, part_number=part_number, seek=seek)
        futures.append(future)

    done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
    if len(not_done) > 0:
        abort_event.set()
    for future in not_done:
        future.cancel()
    for future in done:
        if future.exception() is not None:
            raise future.exception()

    logger.debug("Finalizing multipart upload of %s", local_file)
    response = requests.put(
        multipart_upload.finalize_signed_url.url,
        data=_get_azure_blob_completion_body(
            block_ids=multipart_upload.azure_blob_block_ids
        ),
        timeout=2 * 60,
    )
    response.raise_for_status()
    logger.debug("Multipart upload of %s completed", local_file)


def _any_future_has_failed(futures) -> bool:
    return any(
        future.done() and not future.cancelled() and future.exception() is not None
        for future in futures
    )


class MlFoundryArtifactsRepository(ArtifactRepository):
    def __init__(self, version_id: uuid.UUID, mlflow_client: MlflowClient):
        self.version_id = version_id
        self._tracking_client = mlflow_client
        super().__init__(artifact_uri=None)

    # these methods should be named list_files, log_directory, log_file, etc
    def list_artifacts(
        self, path=None, page_size=_LIST_FILES_PAGE_SIZE, **kwargs
    ) -> typing.Iterator[FileInfo]:
        page_token = None
        started = False
        while not started or page_token is not None:
            started = True
            page = self._tracking_client.list_files_for_artifact_version(
                version_id=self.version_id,
                path=path,
                max_results=page_size,
                page_token=page_token,
            )
            for file_info in page:
                yield file_info
            page_token = page.token

    def log_artifacts(self, local_dir, artifact_path=None):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)

        files_for_normal_upload: List[Tuple[str, str, _FileMultiPartInfo]] = []
        files_for_multipart_upload: List[Tuple[str, str, _FileMultiPartInfo]] = []

        for (root, _, file_names) in os.walk(local_dir):
            upload_path = dest_path
            if root != local_dir:
                rel_path = os.path.relpath(root, local_dir)
                rel_path = relative_path_to_artifact_path(rel_path)
                upload_path = posixpath.join(dest_path, rel_path)
            for file_name in file_names:
                local_file = os.path.join(root, file_name)
                multipart_info = _decide_file_parts(local_file)

                final_upload_path = upload_path or ""
                final_upload_path = final_upload_path.lstrip(posixpath.sep)
                final_upload_path = posixpath.join(
                    final_upload_path, os.path.basename(local_file)
                )

                if multipart_info.num_parts == 1:
                    files_for_normal_upload.append(
                        (final_upload_path, local_file, multipart_info)
                    )
                else:
                    files_for_multipart_upload.append(
                        (final_upload_path, local_file, multipart_info)
                    )

        abort_event = Event()
        with ThreadPoolExecutor(max_workers=_MAX_WORKERS_FOR_UPLOAD) as executor:
            futures = []
            # Note: While this batching is beneficial when there is a large number of files, there is also
            # a rare case risk of the signed url expiring before a request is made to it
            _batch_size = _GENERATE_SIGNED_URL_BATCH_SIZE
            for start_idx in range(0, len(files_for_normal_upload), _batch_size):
                end_idx = min(start_idx + _batch_size, len(files_for_normal_upload))
                if _any_future_has_failed(futures):
                    break
                logger.debug("Generating write signed urls for a batch ...")
                remote_file_paths = [
                    files_for_normal_upload[idx][0] for idx in range(start_idx, end_idx)
                ]
                signed_urls = (
                    self._tracking_client.get_signed_urls_for_artifact_version_write(
                        version_id=self.version_id, paths=remote_file_paths
                    )
                )
                for idx, signed_url in zip(range(start_idx, end_idx), signed_urls):
                    (
                        upload_path,
                        local_file,
                        multipart_info,
                    ) = files_for_normal_upload[idx]
                    future = executor.submit(
                        self._log_artifact,
                        local_file=local_file,
                        artifact_path=upload_path,
                        multipart_info=multipart_info,
                        signed_url=signed_url,
                        abort_event=abort_event,
                        executor_for_multipart_upload=None,
                    )
                    futures.append(future)

            done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
            if len(not_done) > 0:
                abort_event.set()
            for future in not_done:
                future.cancel()
            for future in done:
                if future.exception() is not None:
                    raise future.exception()

            for upload_path, local_file, multipart_info in files_for_multipart_upload:
                self._log_artifact(
                    local_file=local_file,
                    artifact_path=upload_path,
                    signed_url=None,
                    multipart_info=multipart_info,
                    executor_for_multipart_upload=executor,
                )

    def _normal_upload(
        self,
        local_file: str,
        artifact_path: str,
        signed_url: Optional[SignedURL],
        abort_event: Event = None,
    ):
        if not signed_url:
            signed_url = (
                self._tracking_client.get_signed_urls_for_artifact_version_write(
                    version_id=self.version_id, paths=[artifact_path]
                )[0]
            )
        logger.info("Uploading %s to %s", local_file, artifact_path)
        _signed_url_upload_file(
            signed_url=signed_url, local_file=local_file, abort_event=abort_event
        )
        logger.debug("Uploaded %s to %s", local_file, artifact_path)

    def _multipart_upload(
        self,
        local_file: str,
        artifact_path: str,
        multipart_info: _FileMultiPartInfo,
        executor: ThreadPoolExecutor,
        abort_event: Optional[Event] = None,
    ):
        logger.info(
            "Uploading %s to %s using multipart upload", local_file, artifact_path
        )
        multipart_upload = self._tracking_client.create_multipart_upload(
            artifact_version_id=self.version_id,
            path=artifact_path,
            num_parts=multipart_info.num_parts,
        )
        if (
            multipart_upload.storage_provider
            is MultiPartUploadStorageProvider.S3_COMPATIBLE
        ):
            _s3_compatible_multipart_upload(
                multipart_upload=multipart_upload,
                local_file=local_file,
                executor=executor,
                multipart_info=multipart_info,
                abort_event=abort_event,
            )
        elif (
            multipart_upload.storage_provider
            is MultiPartUploadStorageProvider.AZURE_BLOB
        ):
            _azure_multi_part_upload(
                multipart_upload=multipart_upload,
                local_file=local_file,
                executor=executor,
                multipart_info=multipart_info,
                abort_event=abort_event,
            )
        else:
            raise NotImplementedError()

    def _log_artifact(
        self,
        local_file: str,
        artifact_path: Optional[str],
        multipart_info: _FileMultiPartInfo,
        signed_url: Optional[SignedURL] = None,
        abort_event: Optional[Event] = None,
        executor_for_multipart_upload: Optional[ThreadPoolExecutor] = None,
    ):
        if multipart_info.num_parts == 1:
            return self._normal_upload(
                local_file=local_file,
                artifact_path=artifact_path,
                signed_url=signed_url,
                abort_event=abort_event,
            )

        if not executor_for_multipart_upload:
            with ThreadPoolExecutor(max_workers=_MAX_WORKERS_FOR_UPLOAD) as executor:
                return self._multipart_upload(
                    local_file=local_file,
                    artifact_path=artifact_path,
                    executor=executor,
                    multipart_info=multipart_info,
                )

        return self._multipart_upload(
            local_file=local_file,
            artifact_path=artifact_path,
            executor=executor_for_multipart_upload,
            multipart_info=multipart_info,
        )

    def log_artifact(self, local_file: str, artifact_path: Optional[str] = None):
        self._log_artifact(
            local_file=local_file,
            artifact_path=artifact_path,
            multipart_info=_decide_file_parts(local_file),
        )

    def _is_directory(self, artifact_path):
        for _ in self.list_artifacts(artifact_path, page_size=3):
            return True
        return False

    def download_artifacts(self, artifact_path, dst_path=None, overwrite: bool = False):
        """
        Download an artifact file or directory to a local directory if applicable, and return a
        local path for it. The caller is responsible for managing the lifecycle of the downloaded artifacts.

        Args:
            artifact_path: Relative source path to the desired artifacts.
            dst_path: Absolute path of the local filesystem destination directory to which to
                             download the specified artifacts. This directory must already exist.
                             If unspecified, the artifacts will either be downloaded to a new
                             uniquely-named directory on the local filesystem or will be returned
                             directly in the case of the LocalArtifactRepository.
            overwrite: if to overwrite the files at/inside `dst_path` if they exist

        Returns:
            str: Absolute path of the local filesystem location containing the desired artifacts.
        """
        is_dir_temp = False
        if dst_path is None:
            dst_path = tempfile.mkdtemp()
            is_dir_temp = True

        dst_path = os.path.abspath(dst_path)
        if is_dir_temp:
            logger.info(
                f"Using temporary directory {dst_path} as the download directory"
            )

        if not os.path.exists(dst_path):
            raise MlFoundryException(
                message=(
                    "The destination path for downloaded artifacts does not"
                    " exist! Destination path: {dst_path}".format(dst_path=dst_path)
                ),
            )
        elif not os.path.isdir(dst_path):
            raise MlFoundryException(
                message=(
                    "The destination path for downloaded artifacts must be a directory!"
                    " Destination path: {dst_path}".format(dst_path=dst_path)
                ),
            )

        try:
            # Check if the artifacts points to a directory
            if self._is_directory(artifact_path):
                futures = []
                file_paths: List[Tuple[str, str]] = []
                abort_event = Event()

                # Check if any file is being overwritten before downloading them
                for file_path, download_dest_path in self._get_file_paths_recur(
                    src_artifact_dir_path=artifact_path, dst_local_dir_path=dst_path
                ):
                    final_file_path = os.path.join(download_dest_path, file_path)

                    # There would be no overwrite if temp directory is being used
                    if (
                        not is_dir_temp
                        and os.path.exists(final_file_path)
                        and not overwrite
                    ):
                        raise MlFoundryException(
                            f"File already exists at {final_file_path}, aborting download "
                            f"(set `overwrite` flag to overwrite this and any subsequent files)"
                        )
                    file_paths.append((file_path, download_dest_path))
                with ThreadPoolExecutor(_MAX_WORKERS_FOR_DOWNLOAD) as executor:
                    # Note: While this batching is beneficial when there is a large number of files, there is also
                    # a rare case risk of the signed url expiring before a request is made to it
                    batch_size = _GENERATE_SIGNED_URL_BATCH_SIZE
                    for start_idx in range(0, len(file_paths), batch_size):
                        end_idx = min(start_idx + batch_size, len(file_paths))
                        if _any_future_has_failed(futures):
                            break
                        logger.debug(f"Generating read signed urls for a batch ...")
                        remote_file_paths = [
                            file_paths[idx][0] for idx in range(start_idx, end_idx)
                        ]
                        signed_urls = self._tracking_client.get_signed_urls_for_artifact_version_read(
                            version_id=self.version_id, paths=remote_file_paths
                        )
                        for idx, signed_url in zip(
                            range(start_idx, end_idx), signed_urls
                        ):
                            file_path, download_dest_path = file_paths[idx]
                            future = executor.submit(
                                self._download_artifact,
                                src_artifact_path=file_path,
                                dst_local_dir_path=download_dest_path,
                                signed_url=signed_url,
                                abort_event=abort_event,
                            )
                            futures.append(future)

                    done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
                    if len(not_done) > 0:
                        abort_event.set()
                    for future in not_done:
                        future.cancel()
                    for future in done:
                        if future.exception() is not None:
                            raise future.exception()

                    output_dir = os.path.join(dst_path, artifact_path)
                    return output_dir
            else:
                return self._download_artifact(
                    src_artifact_path=artifact_path,
                    dst_local_dir_path=dst_path,
                    signed_url=None,
                )
        except Exception as err:
            if is_dir_temp:
                logger.info(
                    f"Error encountered, removing temporary download directory at {dst_path}"
                )
                rmtree(dst_path)  # remove temp directory alongside it's contents
            raise err

    # noinspection PyMethodOverriding
    def _download_file(
        self,
        remote_file_path: str,
        local_path: str,
        signed_url: Optional[SignedURL],
        abort_event: Event = None,
    ):
        def abort_event_callback():
            if abort_event and abort_event.is_set():
                raise Exception("aborting download")

        if not remote_file_path:
            raise MlFoundryException(
                f"remote_file_path cannot be None or empty str {remote_file_path}"
            )
        if not signed_url:
            signed_url = (
                self._tracking_client.get_signed_urls_for_artifact_version_read(
                    version_id=self.version_id, paths=[remote_file_path]
                )[0]
            )
        logger.info("Downloading %s to %s", remote_file_path, local_path)
        _download_file_using_http_uri(
            http_uri=signed_url.url,
            download_path=local_path,
            callback=abort_event_callback,
        )
        logger.debug("Downloaded %s to %s", remote_file_path, local_path)

    def _download_artifact(
        self,
        src_artifact_path,
        dst_local_dir_path,
        signed_url: Optional[SignedURL],
        abort_event=None,
    ):
        """
        Download the file artifact specified by `src_artifact_path` to the local filesystem
        directory specified by `dst_local_dir_path`.
        :param src_artifact_path: A relative, POSIX-style path referring to a file artifact
                                    stored within the repository's artifact root location.
                                    `src_artifact_path` should be specified relative to the
                                    repository's artifact root location.
        :param dst_local_dir_path: Absolute path of the local filesystem destination directory
                                    to which to download the specified artifact. The downloaded
                                    artifact may be written to a subdirectory of
                                    `dst_local_dir_path` if `src_artifact_path` contains
                                    subdirectories.
        :return: A local filesystem path referring to the downloaded file.
        """
        local_destination_file_path = self._create_download_destination(
            src_artifact_path=src_artifact_path, dst_local_dir_path=dst_local_dir_path
        )
        self._download_file(
            remote_file_path=src_artifact_path,
            local_path=local_destination_file_path,
            signed_url=signed_url,
            abort_event=abort_event,
        )
        return local_destination_file_path

    def _get_file_paths_recur(self, src_artifact_dir_path, dst_local_dir_path):
        local_dir = os.path.join(dst_local_dir_path, src_artifact_dir_path)
        dir_content = (
            [  # prevent infinite loop, sometimes the dir is recursively included
                file_info
                for file_info in self.list_artifacts(src_artifact_dir_path)
                if file_info.path != "." and file_info.path != src_artifact_dir_path
            ]
        )
        if not dir_content:  # empty dir
            if not os.path.exists(local_dir):
                os.makedirs(local_dir, exist_ok=True)
        else:
            for file_info in dir_content:
                if file_info.is_dir:
                    yield from self._get_file_paths_recur(
                        src_artifact_dir_path=file_info.path,
                        dst_local_dir_path=dst_local_dir_path,
                    )
                else:
                    yield file_info.path, dst_local_dir_path
