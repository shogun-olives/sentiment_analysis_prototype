"""
Module for checking if files or directories exist
"""
import os


def exists(
        fn: str
) -> bool:
    """
    Checks if a file or directory exists
    :param fn: file or directory name
    :return: True if file exists and has data, otherwise False
    """
    if not os.path.exists(fn):
        return False

    if os.path.isdir(fn):
        if len(os.listdir(fn)) == 0:
            return False
    else:
        if os.path.getsize(fn) == 0:
            return False

    return True


def dir_exists(
        src_dir: str
) -> bool:
    """
    Checks if a directory exists
    :param src_dir: source directory
    :return: True if directory exists and has data, otherwise False
    """
    if not os.path.exists(src_dir):
        return False

    if len(os.listdir(src_dir)) == 0:
        return False
    
    return True


def file_exists(
        fn: str
) -> bool:
    """
    Checks if a file exists
    :param fn: file name
    :return: True if file exists and has data, otherwise False
    """
    if not os.path.exists(fn):
        return False

    if os.path.getsize(fn) == 0:
        return False

    return True


def existing_from_list(
        src_dir: str,
        fns: list[str]
) -> list[str] | None:
    """
    Gets a list of files in fns that already exist in src_dir
    :param src_dir: directory to search in
    :param fns: list of file names to search for in src_dir
    :return: list of files that exist in src_dir
    """
    if not dir_exists(src_dir):
        return None

    fns = [os.path.basename(file) for file in fns]
    src_fns = os.listdir(src_dir)

    return [file for file in fns if file in src_fns]


def not_existing_from_list(
        src_dir: str,
        fns: list[str]
) -> list[str] | None:
    """
    Gets a list of files in fns that do not exist in src_dir
    :param src_dir: directory to search in
    :param fns: list of file names to search for in src_dir
    :return: list of files that don't exist in src_dir
    """
    if not dir_exists(src_dir):
        return None

    fns = [os.path.basename(file) for file in fns]
    src_fns = os.listdir(src_dir)

    return [file for file in fns if file not in src_fns]