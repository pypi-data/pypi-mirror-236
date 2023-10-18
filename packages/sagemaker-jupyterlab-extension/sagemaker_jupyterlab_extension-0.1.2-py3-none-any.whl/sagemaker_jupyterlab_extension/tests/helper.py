import os
import json
from pathlib import Path

""""
This creates a temporary log file in the test folder, 
make sure to cleanup later by invoking the cleanup function and pass right path
"""


def set_log_file_directory(env_var):
    log_path = Path(__file__).parents[0]
    os.environ[env_var] = str(log_path)
    return log_path


"""Read the last entry from the temporary logfile"""


def get_last_entry(file_name):
    with open(file_name) as fid:
        lines = fid.readlines()
    return json.loads(lines[-1])


"""Remove the temporary logfile"""


def remove_temp_file_and_env(logile, env_var):
    os.remove(logile)
    del os.environ[env_var]
