import asyncio

from async_lru import alru_cache
from sagemaker_jupyterlab_extension_common.clients import (
    get_sagemaker_client,
)

"""
This utlility file provides methods for caching purpose for the gitclone handler.  
The current TTL is set to 3600 secs.
"""


@alru_cache(maxsize=1, ttl=60)
async def _get_domain_repositories():
    response = await get_sagemaker_client().describe_domain()
    domain_repos = (
        response.get("DefaultUserSettings", {})
        .get("JupyterLabAppSettings", {})
        .get("CodeRepositories", [])
    )
    domain_repo_list = list(repo["RepositoryUrl"] for repo in domain_repos)
    return domain_repo_list


@alru_cache(maxsize=1, ttl=60)
async def _get_user_profile_repositories():
    response = await get_sagemaker_client().describe_user_profile()
    user_profile_repos = (
        response.get("UserSettings", {})
        .get("JupyterLabAppSettings", {})
        .get("CodeRepositories", [])
    )
    profile_repo_list = list(repo["RepositoryUrl"] for repo in user_profile_repos)
    return profile_repo_list
