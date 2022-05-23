import os
import pwd
import shutil
import subprocess
from pathlib import Path
from typing import Tuple, Union

import yaml

from utils import log


def run(*args, check=True, **kwargs):
    """Ensure that any errors in commands are propagated."""
    return subprocess.run(*args, check=check, **kwargs)


def run_in_own_shells(*statements: str):
    """Run each statement in its own separate shell"""
    for stmt in statements:
        run(stmt, shell=True)


def expand(text: str) -> str:
    """Expand any environment variables and ~ characters."""
    return os.path.expandvars(os.path.expanduser(text))


def user_id_and_group_id(username: str) -> Tuple[int, int]:
    """
    Return a user's id and their primary group's id.
    Equivalent to `id -u` and `id -g`, respectively.
    """
    pw = pwd.getpwnam(username)
    return pw.pw_uid, pw.pw_gid


def recursive_chown(top: Path, owner: str, group: str):
    """
    Recursively change the owner of a directory and its contents, following symlinks.
    Equivalent to `chown -RL`.
    """
    for dirpath, dirnames, filenames in os.walk(top, followlinks=True):
        shutil.chown(dirpath, owner, group)
        for filename in filenames:
            shutil.chown(os.path.join(dirpath, filename), owner, group)


def load_yaml(path: Path) -> Union[dict, list]:
    with path.open() as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError:
            log.EXCEPTION(f'Invalid YAML file: {path.as_posix()}')
            exit(1)
