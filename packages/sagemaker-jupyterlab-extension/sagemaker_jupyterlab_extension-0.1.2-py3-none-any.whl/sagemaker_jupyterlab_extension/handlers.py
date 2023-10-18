import json
import psutil
import tornado
import os
import asyncio
import traceback

from functools import reduce
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from sagemaker_jupyterlab_extension.utils.git_clone_util import (
    _get_domain_repositories,
    _get_user_profile_repositories,
)

DEFAULT_HOME_DIRECTORY = "/home/sagemaker-user"
CPU_USAGE_INTERVAL = 0.1


class InstanceMetricsHandler(JupyterHandler):
    """
    Schema for the resource usage api response

    response_json = {
        metrics: {
            memory: {
                rss_in_bytes: int,
                total_in_bytes: int,
                memory_percentage: float
            },
            cpu: {
                cpu_count: int,
                cpu_percentage: float
            },
            storage: {
                free_space_in_bytes: int,
                used_space_in_bytes: int,
                total_space_in_bytes: int
            }
        }
    }
    """

    executor = ThreadPoolExecutor(max_workers=5)

    """
         Function to calculate the cpu utilization percentage.
         Check official documentation here - https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
    """

    @run_on_executor
    def _get_cpu_percent(self):
        try:
            cpu_percent = psutil.cpu_percent(CPU_USAGE_INTERVAL, percpu=False)
            self.log.info(f"Successfuly retirved cpu percentage {cpu_percent}")
        except Exception as err:
            self.log.exception(f"Failed to get cpu percent: {err}")
            cpu_percent = null
        return cpu_percent

    """
         This function returns the disk usage for the given path.
         Check official documentation here - https://psutil.readthedocs.io/en/latest/#psutil.disk_usage
    """

    def _get_disk_usage(self):
        try:
            path = os.environ.get("HOME_DIRECTORY", DEFAULT_HOME_DIRECTORY)
            self.log.info(f"Retrieved path {path}")
            disk_usage = psutil.disk_usage(path)
            self.log.info(f"Successfuly retirved disk usage {disk_usage}")
            return {
                "free_space_in_bytes": disk_usage.free,
                "used_space_in_bytes": disk_usage.used,
                "total_space_in_bytes": disk_usage.total,
            }
        except Exception as err:
            self.log.exception(f"Failed to retrieve disk usage: {err}")
            return {}

    """
         This function returns the statistics about the system memory usage.
         Check official documentation here - https://psutil.readthedocs.io/en/latest/#psutil.virtual_memory
    """

    def _get_memory_usage(self):
        try:
            memory = psutil.virtual_memory()
            self.log.info(f"Successfuly retirved memory usage {memory}")
            return {
                "rss_in_bytes": memory.used,
                "total_in_bytes": memory.total,
                "memory_percentage": memory.percent,
            }
        except Exception as err:
            self.log.exception(f"Failed to retrieve memory usage: {err}")
            return {}

    @tornado.web.authenticated
    async def get(self):
        """
        Calculate and return the CPU, Memory and Disk usage for the Instance.
        :return: Response object compliant with above defined schema
        """

        curr_process = psutil.Process()

        if curr_process is None:
            self.set_status(500)
            self.finish(json.dumps({"error": "No parent process found"}))

        """
        Get memory information for an instance.
        """

        memory_metrics = self._get_memory_usage()

        """
        Get CPU utilization
        """

        cpu_count = psutil.cpu_count()
        if cpu_count is None:
            cpu_count = null
        cpu_percent = await self._get_cpu_percent()
        cpu_metrics = {"cpu_count": cpu_count, "cpu_percentage": cpu_percent}

        """
            Get Disk Usage 
        """
        storage_metrics = self._get_disk_usage()

        metrics_response = {
            "metrics": {
                "memory": memory_metrics,
                "cpu": cpu_metrics,
                "storage": storage_metrics,
            }
        }
        self.set_status(200)
        self.finish(json.dumps(metrics_response))


def build_url(web_app, endpoint):
    base_url = web_app.settings["base_url"]
    return url_path_join(base_url, endpoint)


def register_handlers(nbapp):
    web_app = nbapp.web_app
    host_pattern = ".*$"
    handlers = [
        (
            build_url(web_app, r"/aws/sagemaker/api/instance/metrics"),
            InstanceMetricsHandler,
        ),
        (
            build_url(web_app, r"/aws/sagemaker/api/git/list-repositories"),
            GitCloneHandler,
        ),
    ]
    web_app.add_handlers(host_pattern, handlers)


class GitCloneHandler(JupyterHandler):
    """
    Response schema for the GitRepoList API
    {
        "GitCodeRepositories": [
            "repo1",
            "repo2"
        ]
    }

    """

    """
     Function to retrieve git repostiories from domain settings
    """

    async def _get_repositories_from_domain(self):
        repo_list = []
        try:
            self.log.info("Fetching repositories from domain settings")
            response = await _get_domain_repositories()
            if not response:
                self.log.warning(f"No git repositories found in domain settings")
            else:
                self.log.info(
                    "Successfully fetched %s repositories from domain setting",
                    len(response),
                )
                repo_list = response
        except Exception as error:
            self.log.error(
                (
                    "Failed to describe domain with exception: {0}".format(
                        traceback.format_exc()
                    )
                )
            )
        return list(set(repo_list))

    """
     Function to retrieve git repostiories from user setting in user-profile
    """

    async def _get_repositories_from_user_profile(self):
        repo_list = []
        try:
            self.log.info("Fetching repositories from user-profile settings")
            response = await _get_user_profile_repositories()
            if not response:
                self.log.warning(f"No git repositories found in user profile settings")
            else:
                self.log.info(
                    "Successfully fetched %s repositories from user profile settings",
                    len(response),
                )
                repo_list = response
        except Exception as error:
            self.log.error(
                (
                    "Failed to describe user-profile with exception: {0}".format(
                        traceback.format_exc()
                    )
                )
            )
        return list(set(repo_list))

    @tornado.web.authenticated
    async def get(self):
        domain_repositories = self._get_repositories_from_domain()
        user_profile_repositories = self._get_repositories_from_user_profile()
        try:
            result = await asyncio.gather(
                domain_repositories, user_profile_repositories
            )
            res = reduce(lambda a, b: a + b, result)
            self.set_status(200)
            self.finish(json.dumps({"GitCodeRepositories": res}))
        except Exception as error:
            self.log.error(error)
            self.set_status(500)
            self.finish(json.dumps({"error": "Internal Server error occured"}))
