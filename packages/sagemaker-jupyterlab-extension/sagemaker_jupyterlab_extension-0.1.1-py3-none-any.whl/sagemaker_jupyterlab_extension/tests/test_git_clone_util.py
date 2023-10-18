import json
import pytest
import tornado
import asyncio

from unittest.mock import ANY, Mock, patch, MagicMock, AsyncMock
from sagemaker_jupyterlab_extension.utils.git_clone_util import (
    _get_domain_repositories,
    _get_user_profile_repositories,
)

DESCRIBE_USER_PROFILE_TEST_RESPONSE = {
    "UserSettings": {
        "JupyterLabAppSettings": {
            "DefaultResourceSpec": {
                "SageMakerImageArn": "arn:aws:sagemaker:us-east-2:112233445566:image/jupyter-server-3",
                "InstanceType": "system",
            },
            "CodeRepositories": [
                {"RepositoryUrl": "https://github.com/user/userporifle.git"}
            ],
        },
    }
}

DESCRIBE_USER_PROFILE_TEST_RESPONSE_NO_REPOSITORIES = {"UserSettings": {}}


DESCRIBE_DOMAIN_TEST_RESPONSE = {
    "DefaultUserSettings": {
        "JupyterLabAppSettings": {
            "DefaultResourceSpec": {
                "SageMakerImageArn": "arn:aws:sagemaker:us-east-2:112233445566:image/jupyter-server-3",
                "InstanceType": "system",
            },
            "CodeRepositories": [
                {"RepositoryUrl": "https://github.com/domain/domain.git"}
            ],
        },
    }
}


TEST_DOMAIN_RESPONSE = ["https://github.com/domain/domain.git"]


TEST_USER_PROFILE_RESPONSE = ["https://github.com/user/userporifle.git"]


class SageMakerClientMock:
    domain_response: any
    user_profile_response: any

    def __init__(self, domain_resp, user_profile_resp):
        self.domain_response = domain_resp
        self.user_profile_response = user_profile_resp

    async def describe_domain(self):
        return self.domain_response

    async def describe_user_profile(self):
        return self.user_profile_response


@pytest.mark.asyncio
@patch("sagemaker_jupyterlab_extension.utils.git_clone_util.get_sagemaker_client")
async def test_get_domain_repositories(sagemaker_client_mock):
    sagemaker_client_mock.return_value = SageMakerClientMock(
        DESCRIBE_DOMAIN_TEST_RESPONSE, DESCRIBE_USER_PROFILE_TEST_RESPONSE
    )
    _get_domain_repositories.cache_clear()
    response = await _get_domain_repositories()
    assert response == TEST_DOMAIN_RESPONSE


@pytest.mark.asyncio
@patch("sagemaker_jupyterlab_extension.utils.git_clone_util.get_sagemaker_client")
async def test_get_user_profile_repositories(sagemaker_client_mock):
    sagemaker_client_mock.return_value = SageMakerClientMock(
        DESCRIBE_DOMAIN_TEST_RESPONSE, DESCRIBE_USER_PROFILE_TEST_RESPONSE
    )
    _get_user_profile_repositories.cache_clear()
    response = await _get_user_profile_repositories()
    assert response == TEST_USER_PROFILE_RESPONSE


@pytest.mark.asyncio
@patch("sagemaker_jupyterlab_extension.utils.git_clone_util.get_sagemaker_client")
async def test_get_user_profile_repositories_return_empty_json(sagemaker_client_mock):
    sagemaker_client_mock.return_value = SageMakerClientMock(
        DESCRIBE_DOMAIN_TEST_RESPONSE,
        DESCRIBE_USER_PROFILE_TEST_RESPONSE_NO_REPOSITORIES,
    )
    _get_user_profile_repositories.cache_clear()
    response = await _get_user_profile_repositories()
    assert response == []
