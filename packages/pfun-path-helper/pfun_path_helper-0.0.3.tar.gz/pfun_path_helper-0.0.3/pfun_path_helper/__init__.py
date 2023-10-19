"""pfun_path_helper"""
import sys
from typing import Optional
import os
import pkg_resources
from setuptools import find_packages
from site import getsitepackages
import difflib
import importlib
import logging

# setup logging
logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def guess_package_root(directory_path=None, m=3):
    """guess the most likely package root, starting from the current directory"""
    cwd = os.path.abspath(os.getcwd())
    if directory_path is None:
        directory_path = cwd
    pkgs = find_packages(where=directory_path)
    path_split = directory_path.split(os.sep)
    if len(pkgs) == 0 and path_split[-1] == path_split[-2]:
        top_dir = os.path.split(directory_path)[0]
        pkgs = find_packages(where=top_dir)
    pkgs = [p for p in pkgs if not p.endswith('tests')]
    if len(pkgs) > 0:
        directory_path = importlib.import_module(pkgs[0]).__path__[0]
        return directory_path
    else:
        n = 0
        # walk up, down the directory tree until we find a directory containing a __init__.py
        # ...or reach m levels of directories
        while n < m:
            for root, _, files in os.walk(directory_path):
                if '__init__.py' in files:
                    return os.path.abspath(root)
            # set new directory path (up a level)
            directory_path = os.path.abspath(os.path.join(directory_path, '..'))
            n += 1
        return cwd


def get_lib_path(package_name: Optional[str] = None,
                 directory_path: Optional[str] = None) -> str:
    """
    Get the path of a Python package.

    Args:
        package_name (str, optional): The name of the package. If not provided, the first package found in the current directory will be used. Defaults to None.
        directory_path (str, optional): The path to the directory where the package is located. If not provided, the current working directory will be used. Defaults to None.

    Returns:
        str: The path of the package.

    Raises:
        ValueError: If no packages are found in the current directory and no package name or directory location is specified.

    Warnings:
        If the specified package is not found in the specified directory, a warning will be logged and the default package location will be used.
    """
    directory_path = directory_path or guess_package_root()
    if package_name is None:
        pkgs = find_packages(where=directory_path)
        path_split = directory_path.split(os.sep)
        if len(pkgs) == 0 and path_split[-1] == path_split[-2]:
            top_dir = os.path.split(directory_path)[0]
            pkgs = find_packages(where=top_dir)
        pkgs = [p for p in pkgs if p not in ['tests']]
        if len(pkgs) == 0:
            raise ValueError('No packages found in the specified directory. Please specify a package name or directory location.')
        package_name = pkgs[0]
    if directory_path.endswith(package_name) and \
        os.path.exists(os.path.join(directory_path, package_name, '__init__.py')):
        return os.path.join(directory_path, package_name)
    return directory_path


def append_path(path: Optional[str | os.PathLike] = None) -> list[str]:
    """
    Append a path to the sys.path list.

    Args:
        path (Optional[str | os.PathLike], optional): The path to be appended
        to sys.path. If not provided, the default library path will be used.
        Defaults to None.

    Returns:
        list[str]: The updated sys.path list.
    """
    if path is None:
        path = get_lib_path()
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    parent = os.path.abspath(os.path.join(path, '..')) 
    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))
    return sys.path


#: automatically append the root package directory to sys.path when imported
try:
    append_path()
except Exception:
    logger.warning('Failed to append package path to sys.path. Please check your package name and directory location.')

if __name__ == '__main__':
    print(get_lib_path())
    print(sys.path)
