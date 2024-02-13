"""
This module is used to maneuver data between databases and dataframes
"""

from .shared import find_index, txt_get_symbol
import os
import pandas as pd
import datetime


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
    Extracts a dictionary containing metadata that can be extracted from file name
    :param fn: Name of file
    :return: dictionary containing metadata for data that was found, otherwise, value is None
    """
    # get company name
    company_name = txt_get_comp_name(fn)

    # get presentation type
    presentation_type = txt_get_pres_type(fn)

    # get date
    date = txt_get_date(fn)

    # get id
    conf_id = txt_get_id(fn)

    data = {
        'ID': conf_id,
        'Company': company_name,
        'Date': date,
        'Type': presentation_type,
    }

    return data


def get_metadata(fn: str, directory: str = None) -> dict[str: list[str, None, datetime.date]]:
    """
    Extract metadata from file
    :param fn: name of file
    :param directory: optionally, directory to file
    :return: dictionary containing data that was found, otherwise value is None
    """
    metadata = get_fn_data(fn)
    symbol = txt_get_symbol(fn, directory)

    data = {
        'ID': [metadata['ID']],
        'Company': [metadata['Company']],
        'Symbol': [symbol],
        'Date': [metadata['Date']],
        'Type': [metadata['Type']],
    }

    return data


def get_metadata_df(directory: str) -> pd.DataFrame:
    """
    Extracts metadata from all files in a directory as pandas dataframe
    :param directory: directory to extract from
    :return: pandas dataframe
    """
    # empty array to store data
    data = []

    # for each file, try to extract metadata
    for file in os.listdir(directory):
        row = get_metadata(file, directory)
        data.append(pd.DataFrame.from_dict(row))

    # concatenate all data into a dataframe
    df = pd.concat(data)

    return df