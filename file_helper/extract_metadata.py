"""
This module is used to maneuver data between databases and dataframes
"""

from .shared import get_fn_data, get_symbol
import os
import pandas as pd
from datetime import datetime


def get_metadata(fn: str, directory: str = None) -> dict[str: list[str, None, datetime.date]]:
    """
    Extract metadata from file
    :param fn: name of file
    :param directory: optionally, directory to file
    :return: dictionary containing data that was found, otherwise value is None
    """
    metadata = get_fn_data(fn)
    symbol = get_symbol(fn, directory)

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