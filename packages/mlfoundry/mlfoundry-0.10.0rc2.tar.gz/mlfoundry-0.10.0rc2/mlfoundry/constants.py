import datetime
import os
import posixpath
from pathlib import Path

from mlfoundry.internal_namespace import NAMESPACE

DEFAULT_TRACKING_URI = "https://app.truefoundry.com"
RUN_LOGS_DIR = posixpath.join("mlf", "run-logs")


# TODO (chiragjn): This should be run specific, otherwise this will only be initialised once per
#                   interpreter
MLFOUNDRY_TMP_FOLDER = Path(os.path.abspath("./.mlfoundry"))
RUN_TMP_FOLDER = Path(
    os.path.join(MLFOUNDRY_TMP_FOLDER, "logdirs")
)  # this is the log directory

RUN_PREDICTIONS_FOLDER = Path(
    os.path.join(RUN_TMP_FOLDER, "predictions")
)  # path to store predictions
RUN_DATASET_FOLDER = Path(
    os.path.join(RUN_TMP_FOLDER, "datasets")
)  # path to store datasets
# path to store dataset stats
RUN_STATS_FOLDER = Path(os.path.join(RUN_TMP_FOLDER, "stats"))
RUN_METRICS_FOLDER = Path(os.path.join(RUN_TMP_FOLDER, "metrics"))

GET_RUN_TMP_FOLDER = Path(
    os.path.join(MLFOUNDRY_TMP_FOLDER, "getdirs")
)  # this is the log directory
GET_RUN_PREDICTIONS_FOLDER = Path(
    os.path.join(GET_RUN_TMP_FOLDER, "predictions")
)  # path to store predictions
GET_RUN_DATASET_FOLDER = Path(
    os.path.join(GET_RUN_TMP_FOLDER, "datasets")
)  # path to store datasets

TIME_LIMIT_THRESHOLD = datetime.timedelta(minutes=1)
FILE_SIZE_LIMIT_THRESHOLD = pow(10, 7)  # 10MB

MULTI_DIMENSIONAL_METRICS = "multi_dimensional_metrics"  # multi dimensional metrics
NON_MULTI_DIMENSIONAL_METRICS = (
    "non_multi_dimensional_metrics"  # non-multi dimensional metrics
)
PROB_MULTI_DIMENSIONAL_METRICS = (
    "prob_multi_dimensional_metrics"  # multi dimensional metrics
)
PROB_NON_MULTI_DIMENSIONAL_METRICS = (
    "prob_non_multi_dimensional_metrics"  # non-multi dimensional metrics
)

LATEST_ARTIFACT_OR_MODEL_VERSION = "latest"

ACTUAL_PREDICTION_COUNTS = "actuals_predictions_counts"
MLF_FOLDER_NAME = "mlf"
MLRUNS_FOLDER = "mlruns"
MLRUNS_FOLDER_NAME = Path(os.path.join(MLF_FOLDER_NAME, MLRUNS_FOLDER))


# Runs Name and DF constants
RUN_ID_COL_NAME = "run_id"
RUN_NAME_COL_NAME = "run_name"

TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


GIT_COMMIT_TAG_NAME = NAMESPACE("git.commit_sha")
GIT_BRANCH_TAG_NAME = NAMESPACE("git.branch_name")
GIT_REMOTE_URL_NAME = NAMESPACE("git.remote_url")
GIT_DIRTY_TAG_NAME = NAMESPACE("git.dirty")
PATCH_FILE_ARTIFACT_DIR = NAMESPACE / "git"
LOG_DATASET_ARTIFACT_DIR = NAMESPACE / "datasets"
# without .txt patch file does not load on UI
PATCH_FILE_NAME = "uncommitted_changes.patch.txt"

PYTHON_VERSION_TAG_NAME = NAMESPACE("python_version")
MLFOUNDRY_VERSION_TAG_NAME = NAMESPACE("mlfoundry_version")


ALM_SCALAR_METRICS_PATTERN = NAMESPACE("auto_logged_metrics.{data_slice}.{metric_name}")
ALM_ARTIFACT_PATH = NAMESPACE / "auto_logged_metrics"
ALM_METRICS_FILE_NAME = "metrics.json"
