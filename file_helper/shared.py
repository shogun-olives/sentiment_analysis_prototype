"""
This module contains functions that are commonly used throughout this package
"""

import os


def remove_overlap(str1: str, str2: str, split: str) -> (str, str):
    """
    Removes overlap between end of str1 and start of str2 where they are split by str
    :param str1: string to keep
    :param str2: string to remove start from
    :param split: character to split by
    :return: str1, str2 with overlap removed
    """
    arr1 = str1.split(split)
    arr2 = str2.split(split)

    while arr1[-1] == arr2[0]:
        del arr2[0]

    return split.join(arr1), split.join(arr2)


def get_path(fn: str, directory: str = None, get_fn_dir: bool = True) -> str | (str, str, str):
    """
    Ensure that fn and directory are properly split
    :param fn: Name of file
    :param directory: Name of directory
    :param get_fn_dir: Returns path, fn, and dir if True, otherwise just path
    :return: Absolute path to file, File name, Absolute directory
    """
    if directory is not None:
        # get absolute directory path
        directory = os.path.abspath(directory)
        directory_path = os.path.normpath(directory)

        # get relative normpath to fn
        fn_path = os.path.normpath(fn)

        # remove overlap
        directory_path, fn_path = remove_overlap(directory_path, fn_path, "\\")

        # get merged path
        merged_path = os.path.join(directory_path, fn_path)
    else:
        # if no directory, merged path is just absolute path to fn
        fn = os.path.abspath(fn)
        merged_path = os.path.normpath(fn)

    # if not getting fn and dir, just return merged path
    if not get_fn_dir:
        return merged_path

    # gets new directory and dn based on merge
    abs_dir, abs_fn = os.path.split(merged_path)

    return merged_path, abs_fn, abs_dir


def file_exists(fn: str, directory: str = None) -> bool:
    """
    Checks if a file exists in d directory
    :param fn: name of file to search for
    :param directory: directory to search for file in, if left blank, defaults to current working directory
    :return: True if file exists and has data, otherwise False
    """
    # Constructs relative path to given file
    if directory is not None:
        path = os.path.join(directory, fn)
    else:
        path = fn

    # Checks if file exists
    if not os.path.exists(path):
        return False

    # If file exists, checks if file has data
    if os.path.getsize(path) == 0:
        return False

    # if file doesn't exist or has no data, return true
    return True


def existing_files(file_names: list[str], directory: str) -> list[str] | None:
    """
    Gets a list of files that already exist in directory
    :param file_names: list of files to search for in directory
    :param directory: directory to search in
    :return: list of files that exist in directory or None if directory does not exist
    """
    # makes sure that given directory is valid
    try:
        os.listdir(directory)
    except FileNotFoundError:
        return None

    # makes sure file names are just names, not paths
    file_names = [os.path.basename(file) for file in file_names]

    # adds every existing file to an array
    exist = []
    for file in file_names:
        # checks if file exists in directory
        if file_exists(file, directory):
            exist.append(file)

    return exist


def find_index(search_for: list[str], word_arr: list[str]) -> int | None:
    """
    Returns the index of the first item in search for to appear in word_arr
    :param search_for: list of words to search for
    :param word_arr: list of words to search in
    :return: index of first occurrence, otherwise None
    """
    # iterates through words to search for
    for search_word in search_for:
        # try to find value, if not in word_arr, search for next value
        try:
            index = word_arr.index(search_word)
            return index
        except ValueError:
            pass

    # if none of the search words are found in word_arr, return None
    return None