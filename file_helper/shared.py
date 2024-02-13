"""
This module contains functions that are commonly used throughout this package
"""

import os
import datetime


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


def ensure_fn_path(fn: str, directory: str = None) -> (str, str, str):
    """
    Ensure that fn and directory are properly split
    :param fn: Name of file
    :param directory: Name of directory
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


def get_symbol(fn: str, directory: str = None) -> str | None:
    """
    Gets the stock symbol of a transcript by reading its first two lines
    :param fn: name of file to extract stock symbol from
    :param directory: directory to search for file in, if left blank, defaults to current working directory
    :return: Stock symbol if found, otherwise None
    """
    path, fn, directory = ensure_fn_path(fn, directory)

    # opens file
    with open(path, 'r', encoding='utf-8') as file:
        # reads first two lines
        for _ in range(2):
            line = file.readline()

        # converts line into list
        words = line.split(' ')

        # 2nd line of file always contains
        #   [Company Name] ([Stock Symbol] US Equity)
        # searching for "(" will reliably find the stock symbol
        for word in words:
            if '(' in word:
                # once "(" is found, remove it from prefix
                word = word.removeprefix('(')

                # if potential symbol is longer than 4 char, only get first 4 chars
                if len(word) > 4:
                    word = word[:4]

                # return constructed symbol
                return word

    # if no "(" is found, method failed and None is returned
    return None


def company_name_from_fn(fn: str) -> str | None:
    """
    Extracts company name from file name
    :param fn: Name of file
    :return: company name if found, otherwise None
    """
    # separate file name from path in case user mistake
    fn = os.path.basename(fn)

    # separate words in title based on space
    words = fn.removesuffix('.txt').split(' ')

    # searches for company name based on suffixes
    comp_suffixes = ['Inc', 'Corp']
    comp_end_index = find_index(comp_suffixes, words)

    # constructs company name
    if comp_end_index is not None:
        company_name = ' '.join(words[:comp_end_index + 1])
    else:
        company_name = None

    return company_name


def presentation_type_from_fn(fn: str) -> str | None:
    """
    Extracts presentation type from file name
    :param fn: Name of file
    :return: presentation type if found, otherwise None
    """
    # separate file name from path in case user mistake
    fn = os.path.basename(fn)

    # separate words in title based on space
    words = fn.removesuffix('.txt').split(' ')

    # searches for company name based on suffixes
    comp_suffixes = ['Inc', 'Corp']
    comp_end_index = find_index(comp_suffixes, words)

    # searches for presentation type name based on suffixes
    pres_suffixes = ['Day', 'Call']
    pres_end_index = find_index(pres_suffixes, words)

    # constructs presentation type
    if comp_end_index is not None and pres_end_index is not None:
        presentation_name = ' '.join(words[(comp_end_index + 1):(pres_end_index + 1)])
    else:
        presentation_name = None

    return presentation_name


def date_from_fn(fn: str) -> datetime.date | None:
    """
    Extracts date from file name
    :param fn: Name of file
    :return: date if found, otherwise None
    """
    # separate file name from path in case user mistake
    fn = os.path.basename(fn)

    # separate words in title based on space
    words = fn.removesuffix('.txt').split(' ')

    # checks if format is valid
    date_str = words[-2]
    if not date_str.isdigit() or len(date_str) < 7:
        return None

    # constructs date
    yr = int(date_str[:4])
    month = int(date_str[4:-2])
    day = int(date_str[-2:])
    date = datetime.date(yr, month, day)

    return date


def id_from_fn(fn: str) -> str:
    """
    Extracts id from file name
    :param fn: Name of file
    :return: id if found, otherwise None
    """
    # separate file name from path in case user mistake
    fn = os.path.basename(fn)

    # separate words in title based on space
    words = fn.removesuffix('.txt').split(' ')

    # id is the last item in the title
    id_str = words[-1]

    return id_str


def get_fn_data(fn: str) -> dict[str: str | datetime.date | None]:
    """
    Extracts a dictionary containing metadata that can be extracted from file name
    :param fn: Name of file
    :return: dictionary containing metadata for data that was found, otherwise, value is None
    """
    # get company name
    company_name = company_name_from_fn(fn)

    # get presentation type
    presentation_type = presentation_type_from_fn(fn)

    # get date
    date = date_from_fn(fn)

    # get id
    conf_id = id_from_fn(fn)

    data = {
        'ID': conf_id,
        'Company': company_name,
        'Date': date,
        'Type': presentation_type,
    }

    return data