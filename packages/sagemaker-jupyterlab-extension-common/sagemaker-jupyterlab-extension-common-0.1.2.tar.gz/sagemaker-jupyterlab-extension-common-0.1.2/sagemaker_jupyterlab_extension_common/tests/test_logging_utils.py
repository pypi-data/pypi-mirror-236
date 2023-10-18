import sys
import logging
import os
import traceback
from unittest.mock import patch, mock_open

from sagemaker_jupyterlab_extension_common.constants import (
    SERVER_LOG_SCHEMA,
    HANDLER_METRICS_SCHEMA,
    REQUEST_METRICS_SCHEMA,
    LOGFILE_ENV_NAME,
    SERVER_LOG_FILE_NAME,
    API_LOG_FILE_NAME,
)
from sagemaker_jupyterlab_extension_common.logging.logging_utils import (
    get_operational_logger,
    get_eventlog,
    get_metric_writer,
    OperationalLoggingHandler,
)

from sagemaker_jupyterlab_extension_common.logging.logging_utils import (
    HandlerLogMixin,
)

from .utils import (
    get_last_entry,
    set_log_file_directory,
    remove_temp_file_and_env,
)


@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_domain_id")
@patch(
    "sagemaker_jupyterlab_extension_common.logging.logging_utils.get_user_profile_name"
)
@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_aws_account_id")
@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_space_name")
def test_operational_logger_valid_event_success(
    mock_space,
    mock_aws_account,
    mock_user_profile,
    mock_domain,
):
    mock_space.return_value = "default-space"
    mock_user_profile.return_value = "test-user-profile"
    mock_domain.return_value = "d-jk12345678"
    mock_aws_account.return_value = "1234567890"

    # Create a temporary log file for logger to write
    file_path = set_log_file_directory(LOGFILE_ENV_NAME)
    file = os.path.join(file_path.parents[0], SERVER_LOG_FILE_NAME)

    # create logger oject
    obj = object()
    logger = get_operational_logger(
        obj, eventlog=get_eventlog(), extension_name="TestEXT", extension_version="1.0"
    )
    logger.setLevel(logging.INFO)
    additional_data = {"Component": "MyTestComponent"}
    # Additional non required attributes can be set by passing dictionary to extra attribute in log.
    logger.info("test_logger", extra=additional_data)

    # read the log file
    data = get_last_entry(file)

    assert data["__schema__"] == SERVER_LOG_SCHEMA
    assert data["Level"] == "INFO"
    assert data["Message"] == "test_logger"
    assert data["Context"]["ExtensionName"] == "TestEXT"
    assert data["Context"]["ExtensionVersion"] == "1.0"
    assert data["Context"]["SpaceName"] == "default-space"
    assert data["Context"]["AccountId"] == "1234567890"
    assert data["Context"]["UserProfileName"] == "test-user-profile"
    assert data["Context"]["DomainId"] == "d-jk12345678"
    assert data["Context"]["Component"] == "MyTestComponent"

    # Should add OperationLogging handler once only
    logger = get_operational_logger(obj, eventlog=get_eventlog())
    handlerCount = len(
        list(
            filter(lambda x: isinstance(x, OperationalLoggingHandler), logger.handlers)
        )
    )
    assert handlerCount == 1

    # Remove the temp file
    remove_temp_file_and_env(file, LOGFILE_ENV_NAME)


# ---------------------------------------------------------------------------
#   TestMixin and Logging
# ---------------------------------------------------------------------------


class TestExtensionLogMixin(HandlerLogMixin):
    def __init__(self, ext_name, ext_version):
        super().__init__(ext_name, ext_version)


@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_domain_id")
@patch(
    "sagemaker_jupyterlab_extension_common.logging.logging_utils.get_user_profile_name"
)
@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_aws_account_id")
@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_space_name")
def test_logging_mixin(
    mock_space,
    mock_aws_account,
    mock_user_profile,
    mock_domain,
):
    mock_space.return_value = "default-space"
    mock_user_profile.return_value = "test-user-profile"
    mock_domain.return_value = "d-jk12345678"
    mock_aws_account.return_value = "1234567890"

    test_ext_name = "test_ext_name"
    test_ext_version = "1.0"

    # Create a temporary log file for logger to write
    file_path = set_log_file_directory(LOGFILE_ENV_NAME)
    file = os.path.join(file_path.parents[0], SERVER_LOG_FILE_NAME)

    logger = TestExtensionLogMixin(test_ext_name, test_ext_version)
    logger.log.error("MyTestErrorLog")

    data = get_last_entry(file)
    assert data["__schema__"] == SERVER_LOG_SCHEMA
    assert data["Level"] == "ERROR"
    assert data["Message"] == "MyTestErrorLog"
    assert data["Context"]["ExtensionName"] == "test_ext_name"
    assert data["Context"]["ExtensionVersion"] == "1.0"
    assert data["Context"]["SpaceName"] == "default-space"
    assert data["Context"]["AccountId"] == "1234567890"
    assert data["Context"]["UserProfileName"] == "test-user-profile"
    assert data["Context"]["DomainId"] == "d-jk12345678"

    # Remove the temp file
    remove_temp_file_and_env(file, LOGFILE_ENV_NAME)


@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_domain_id")
@patch(
    "sagemaker_jupyterlab_extension_common.logging.logging_utils.get_user_profile_name"
)
@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_aws_account_id")
@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_space_name")
@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils._get_event_capsule")
def test_operational_logger_invalid_event_failure(
    mock_event_data,
    mock_space,
    mock_aws_account,
    mock_user_profile,
    mock_domain,
):
    mock_space.return_value = "default-space"
    mock_user_profile.return_value = "test-user-profile"
    mock_domain.return_value = "d-jk12345678"
    mock_aws_account.return_value = "1234567890"
    mock_event_data.return_value = dict(Context={})

    obj = object()
    logger = get_operational_logger(obj, eventlog=get_eventlog())
    logger.setLevel(logging.INFO)
    exception = None
    try:
        logger.info("This event is invalid")
    except Exception as ex:
        exception = ex

    assert exception.__class__.__name__ == "ValidationError"


# ---------------------------------------------------------------------------
#  MetricWriter testing
# ---------------------------------------------------------------------------


@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_domain_id")
@patch(
    "sagemaker_jupyterlab_extension_common.logging.logging_utils.get_user_profile_name"
)
@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_aws_account_id")
@patch("sagemaker_jupyterlab_extension_common.logging.logging_utils.get_space_name")
def test_metric_logger(
    mock_space,
    mock_aws_account,
    mock_user_profile,
    mock_domain,
):
    mock_space.return_value = "default-space"
    mock_user_profile.return_value = "test-user-profile"
    mock_domain.return_value = "d-jk12345678"
    mock_aws_account.return_value = "1234567890"

    # Create a temporary log file for logger to write
    file_path = set_log_file_directory(LOGFILE_ENV_NAME)
    file = os.path.join(file_path.parents[0], API_LOG_FILE_NAME)

    error_context = {
        "MetricName": "Error",
        "MetricValue": 1,
        "MetricUnit": "Count",
        "Dimensions": [
            {
                "Operation": "DescribeCluster",
            },
        ],
    }

    metricWriter = get_metric_writer("extension1", "1.0", "TestNameSpace")

    # write error metric
    metricWriter.put_error("DescribeCluster", **error_context)

    data = get_last_entry(file)
    assert data["__schema__"] == HANDLER_METRICS_SCHEMA
    assert data["Fault"] == 0
    assert data["Context"]["ExtensionName"] == "extension1"
    assert data["Context"]["ExtensionVersion"] == "1.0"
    assert data["Context"]["SpaceName"] == "default-space"
    assert data["Context"]["AccountId"] == "1234567890"
    assert data["Context"]["UserProfileName"] == "test-user-profile"
    assert data["Context"]["DomainId"] == "d-jk12345678"
    assert data["Operation"] == "DescribeCluster"
    assert data["Error"] == 1
    assert data["_aws"]["Timestamp"] > 0
    timestamp = data["_aws"]["Timestamp"]
    assert data["_aws"] == {
        "Timestamp": timestamp,
        "CloudWatchMetrics": [
            {
                "Dimensions": [["Operation"]],
                "Metrics": [{"Name": "Error", "Unit": "Count"}],
                "Namespace": "TestNameSpace",
            }
        ],
    }

    fault_context = {
        "MetricName": "Fault",
        "MetricValue": 1,
        "MetricUnit": "Count",
        "Dimensions": [
            {
                "Operation": "ListCLuster",
            },
        ],
    }

    # Write a fault metrir
    metricWriter.put_fault("ListCLuster", **fault_context)

    data = get_last_entry(file)
    assert data["__schema__"] == HANDLER_METRICS_SCHEMA
    assert data["Context"]["ExtensionName"] == "extension1"
    assert data["Context"]["ExtensionVersion"] == "1.0"
    assert data["Context"]["SpaceName"] == "default-space"
    assert data["Context"]["AccountId"] == "1234567890"
    assert data["Context"]["UserProfileName"] == "test-user-profile"
    assert data["Context"]["DomainId"] == "d-jk12345678"
    assert data["Operation"] == "ListCLuster"
    assert data["Error"] == 0
    assert data["Fault"] == 1
    assert data["_aws"]["Timestamp"] > 0
    timestamp = data["_aws"]["Timestamp"]
    # to verify aws object, reading timestamp from record and assigning in object as value to Timestamp
    assert data["_aws"] == {
        "Timestamp": timestamp,
        "CloudWatchMetrics": [
            {
                "Dimensions": [["Operation"]],
                "Metrics": [{"Name": "Fault", "Unit": "Count"}],
                "Namespace": "TestNameSpace",
            }
        ],
    }

    invalid_context = {
        "MetricName": "Transaction",
        "MetricValue": 1,
        "MetricUnit": "Count",
        "Dimensions": [
            {
                "Operation": "CreatePersistentUI",
            },
        ],
    }

    # Invlaid metric name results into validation error

    metricWriter.put_fault("CreatePersistentUI", **invalid_context)
    data = get_last_entry(file)

    # verify last operation is still fault
    assert data["Operation"] == "ListCLuster"
    assert data["Fault"] == 1

    # Remove the temp file
    remove_temp_file_and_env(file, LOGFILE_ENV_NAME)
