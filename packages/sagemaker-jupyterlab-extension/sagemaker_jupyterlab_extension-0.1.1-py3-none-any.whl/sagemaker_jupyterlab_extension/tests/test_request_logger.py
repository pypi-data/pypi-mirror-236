import os
from unittest.mock import patch
from ..utils.request_logger import (
    sanitize_uri_and_path,
    get_operation_from_uri,
    get_request_metrics_context,
    log_metrics_from_request,
)

from .helper import (
    get_last_entry,
    set_log_file_directory,
    remove_temp_file_and_env,
)

from sagemaker_jupyterlab_extension_common.constants import (
    REQUEST_METRICS_SCHEMA,
)
from sagemaker_jupyterlab_extension_common.constants import (
    REQUEST_METRICS_SCHEMA,
    LOGFILE_ENV_NAME,
    REQUEST_LOG_FILE_NAME,
)


class MockHandler:
    """Minimal API for a handler"""

    def get_status(self):
        return 200


class MockRequest:
    """Minimal API to for a request"""

    uri = "foo"
    path = "foo"
    method = "GET"
    remote_ip = "1.1.1.1"

    def request_time(self):
        return 0.1


def test_sanitize_uri_and_path():
    test_cases = [
        # [ input, expected ]
        [
            "/default/aws/sagemaker/api/git/list-repositories",
            (
                "/default/aws/sagemaker/api/git/list-repositories",
                "/default/aws/sagemaker/api/git/list-repositories",
            ),
        ],
        [
            "/default/aws/sagemaker/api/instance/metrics",
            (
                "/default/aws/sagemaker/api/instance/metrics",
                "/default/aws/sagemaker/api/instance/metrics",
            ),
        ],
        [
            "/default/aws/sagemaker/api/emr/describe-cluster",
            (
                "/default/aws/sagemaker/api/emr/describe-cluster",
                "/default/aws/sagemaker/api/emr/describe-cluster",
            ),
        ],
        [
            "/default/aws/sagemaker/api/emr/list-clusters",
            (
                "/default/aws/sagemaker/api/emr/list-clusters",
                "/default/aws/sagemaker/api/emr/list-clusters",
            ),
        ],
        ["/default/api-that-should-not-be-logged", (None, None)],
    ]
    for test_case in test_cases:
        res = sanitize_uri_and_path(test_case[0])
        assert res == test_case[1]


def test_get_operation_from_uri():
    test_cases = [
        # [ input, expected ]
        [
            ("/default/aws/sagemaker/api/git/list-repositories", "GET"),
            (
                "GET./default/aws/sagemaker/api/git/list-repositories",
                "/default/aws/sagemaker/api/git/list-repositories",
            ),
        ],
        [
            ("/default/aws/sagemaker/api/instance/metrics", "GET"),
            (
                "GET./default/aws/sagemaker/api/instance/metrics",
                "/default/aws/sagemaker/api/instance/metrics",
            ),
        ],
        [
            ("/default/aws/sagemaker/api/emr/describe-cluster", "POST"),
            (
                "POST./default/aws/sagemaker/api/emr/describe-cluster",
                "/default/aws/sagemaker/api/emr/describe-cluster",
            ),
        ],
        [
            ("/default/aws/sagemaker/api/emr/list-clusters", "POST"),
            (
                "POST./default/aws/sagemaker/api/emr/list-clusters",
                "/default/aws/sagemaker/api/emr/list-clusters",
            ),
        ],
        ["/default/aws/some-random-api", (None, None)],
        ["/default/jupyter/internal-api", (None, None)],
    ]
    for test_case in test_cases:
        res = get_operation_from_uri(test_case[0][0], test_case[0][1])
        assert res == test_case[1]


def test_get_request_metrics_context():
    # [ input, expected ]
    test_cases = [
        [
            (
                "/default/aws/sagemaker/api/git/list-repositories",
                "/default/aws/sagemaker/api/git/list-repositories",
                "GET./default/aws/sagemaker/api/git/list-repositories",
                dict(
                    DomainId="test-domain-id",
                    UserProfileName="test-user-profile-name",
                    Status=200,
                    StatusReason="OK",
                ),
            ),
            {
                "Http2xx": 1,
                "Http4xx": 0,
                "Http5xx": 0,
                "Operation": "GET./default/aws/sagemaker/api/git/list-repositories",
                "ResponseLatencyMS": 0.1,
                "UriPath": "/default/aws/sagemaker/api/git/list-repositories",
                "_aws": {
                    "CloudWatchMetrics": [
                        {
                            "Dimensions": [["Operation"]],
                            "Metrics": [
                                {"Name": "ResponseLatencyMS", "Unit": "Seconds"},
                                {"Name": "Http5xx", "Unit": "Count"},
                                {"Name": "Http2xx", "Unit": "Count"},
                                {"Name": "Http4xx", "Unit": "Count"},
                            ],
                            "Namespace": "aws-embedded-metrics",
                        }
                    ],
                    "Timestamp": 123456,
                },
            },
        ]
    ]
    for test_case in test_cases:
        request = MockRequest()
        request.uri = test_case[0][0]
        res = get_request_metrics_context(
            request, test_case[0][1], test_case[0][2], test_case[0][3]
        )
        res["_aws"]["Timestamp"] = 123456
        assert res == test_case[1]


@patch(
    "sagemaker_jupyterlab_extension.utils.request_logger.get_domain_id",
    return_value="d-jk12345678",
)
@patch(
    "sagemaker_jupyterlab_extension.utils.request_logger.get_user_profile_name",
    return_value="test-user-profile",
)
@patch(
    "sagemaker_jupyterlab_extension.utils.request_logger.get_aws_account_id",
    return_value="1234567890",
)
@patch(
    "sagemaker_jupyterlab_extension.utils.request_logger.get_space_name",
    return_value="default-space",
)
def test_log_request(
    mock_space,
    mock_aws_account,
    mock_user_profile,
    mock_domain,
):
    handler = MockHandler()
    request = MockRequest()
    request.path = "/default/aws/sagemaker/api/git/list-repositories"
    request.method = "GET"
    handler.request = request
    # handler.eventlog = None

    # Create a temporary log file for logger to write
    file_path = set_log_file_directory(LOGFILE_ENV_NAME)
    file = os.path.join(file_path.parents[0], REQUEST_LOG_FILE_NAME)

    # Log the metric event
    log_metrics_from_request(handler)

    # Read the last line from log file
    data = get_last_entry(file)

    # Validations
    assert data["__schema__"] == REQUEST_METRICS_SCHEMA
    assert data["Status"] == 200
    assert data["Operation"] == "GET./default/aws/sagemaker/api/git/list-repositories"
    assert data["UriPath"] == "/default/aws/sagemaker/api/git/list-repositories"
    assert data["ResponseLatencyMS"] == 0.1
    assert (
        data["Context"]["ExtensionName"] == "SagemakerStudioJuypterLabExtensionCommon"
    )
    assert data["Context"]["ExtensionVersion"] == "0.1.1"
    assert data["Context"]["AccountId"] == "1234567890"
    assert data["Context"]["DomainId"] == "d-jk12345678"
    assert data["Context"]["UserProfileName"] == "test-user-profile"
    assert data["Context"]["SpaceName"] == "default-space"
    data["_aws"]["Timestamp"] = 123456

    assert data["_aws"] == {
        "CloudWatchMetrics": [
            {
                "Dimensions": [["Operation"]],
                "Metrics": [
                    {"Name": "ResponseLatencyMS", "Unit": "Seconds"},
                    {"Name": "Http5xx", "Unit": "Count"},
                    {"Name": "Http2xx", "Unit": "Count"},
                    {"Name": "Http4xx", "Unit": "Count"},
                ],
                "Namespace": "aws-embedded-metrics",
            }
        ],
        "Timestamp": 123456,
    }

    # Remove the temp file
    remove_temp_file_and_env(file, LOGFILE_ENV_NAME)
