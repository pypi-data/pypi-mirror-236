import click

from mlfoundry import get_client


@click.group(help="Download files of artifact/model logged with Mlfoundry")
def download():
    ...


@download.command(short_help="Download files of logged model")
@click.option(
    "--fqn",
    required=True,
    type=str,
    help="fqn of the model version",
)
@click.option(
    "--path",
    type=click.Path(file_okay=False, dir_okay=True, exists=True),
    default="./",
    show_default=True,
    help="path where the model files will be downloaded",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="flag to overwrite any existing files in the `path` directory",
)
def model(fqn: str, path: str, overwrite: bool):
    """
    Download the files of logged model.\n
    """
    client = get_client()
    model_version = client.get_model_version_by_fqn(fqn=fqn)
    download_path = model_version.download(path=path, overwrite=overwrite)
    print(f"Downloaded model files to {download_path}")


@download.command(short_help="Download files of logged artifact")
@click.option(
    "--fqn",
    required=True,
    type=str,
    help="fqn of the artifact version",
)
@click.option(
    "--path",
    type=click.Path(file_okay=False, dir_okay=True, exists=True),
    default="./",
    show_default=True,
    help="path where the artifact files will be downloaded",
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="flag to overwrite any existing files in the `path` directory",
)
def artifact(fqn: str, path: str, overwrite: bool):
    """
    Download the files of logged artifact.\n
    """
    client = get_client()
    artifact_version = client.get_artifact_version_by_fqn(fqn=fqn)
    download_path = artifact_version.download(path=path, overwrite=overwrite)
    print(f"Downloaded artifact files to {download_path}")
