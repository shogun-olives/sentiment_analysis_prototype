"""
This module is used to extract metadata from txt files
"""

from .shared import find_index, get_path, extract_all
import os
import pandas as pd
import datetime


def txt_get_symbol(fn: str, directory: str = None) -> str | None:
    """
    Gets the stock symbol of a transcript by reading its first two lines
    :param fn: name of file to extract stock symbol from
    :param directory: directory to search for file in, if left blank, defaults to current working directory
    :return: Stock symbol if found, otherwise None
    """
    path = get_path(fn, directory)

    # opens file
    try:
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
    except FileNotFoundError:
        return None
    except PermissionError:
        return None

    # if no "(" is found, method failed and None is returned
    return None


def txt_get_comp_name(fn: str) -> str | None:
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


def txt_get_pres_type(fn: str) -> str | None:
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


def txt_get_date(fn: str) -> datetime.date | None:
    """
    Extracts date from file name
    :param fn: Name of file
    :return: date if found, otherwise None
    """
    # separate file name from path in case user mistake
    fn = os.path.basename(fn)

    # separate words in title based on space
    words = fn.removesuffix('.txt').split(' ')

    # check list length
    if len(words) <= 1:
        return None

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


def txt_get_id(fn: str) -> str:
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
    Extracts a dictionary containing metadata that can be extracted from unformatted txt file
    :param fn: Name of file
    :return: dictionary containing metadata for data that was found, otherwise, value is None
    """
    # gets just file name
    path, fn, directory = get_path(fn, get_fn_dir=True)

    # gets data
    company_name = txt_get_comp_name(fn)
    presentation_type = txt_get_pres_type(fn)
    date = txt_get_date(fn)
    conf_id = txt_get_id(fn)

    data = {
        'ID': conf_id,
        'Company': company_name,
        'Date': date,
        'Type': presentation_type,
    }

    return data


def txt_get_metadata(fn: str, directory: str = None) -> dict[str: list[str, None, datetime.date]]:
    """
    Extract metadata from unformatted txt file
    :param fn: name of file
    :param directory: optionally, directory to file
    :return: dictionary containing data that was found, otherwise value is None
    """
    path, fn, directory = get_path(fn, directory, get_fn_dir=True)

    if not fn.endswith('.txt'):
        return None

    metadata = get_fn_data(fn)
    symbol = txt_get_symbol(fn, directory)

    data = {
        'ID': metadata['ID'],
        'Symbol': symbol,
        'Company': metadata['Company'],
        'Date': metadata['Date'],
        'Type': metadata['Type'],
    }

    return data


def txt_get_all_metadata(directory: str) -> pd.DataFrame:
    """
    Extracts metadata from all files in a directory as pandas dataframe
    :param directory: directory to extract from
    :return: pandas dataframe
    """
    # completes operation on files in directory
    df = extract_all(txt_get_metadata, directory)
    return df