"""
This module is used to extract metadata from csv files
"""
import pandas as pd
from .shared import get_path, extract_all
from datetime import datetime
import re


def csv_get_comp_name(fn: str, directory: str = None) -> str | None:
    """
    Extract company name from csv file
    :param fn: file name
    :param directory: directory name
    :return: company name if found, otherwise None
    """
    path = get_path(fn, directory)

    try:
        with open(path, 'r') as file:
            line = file.readline()
    except FileNotFoundError:
        return None
    except PermissionError:
        return None

    title = line.split(" | ")[0]

    return title


def csv_get_symbol(fn: str, directory: str = None) -> str | None:
    """
    Extract company symbol from csv file
    :param fn: file name
    :param directory: directory name
    :return: company symbol if found, otherwise None
    """
    path = get_path(fn, directory)
    line = "\n"

    try:
        with open(path, 'r') as file:
            while ".O" not in line:
                line = file.readline()

                if not line:
                    return None

                line = line.split(",")[0]

    except FileNotFoundError:
        return None
    except PermissionError:
        return None

    symbol = line.removesuffix(".O")

    return symbol


def csv_get_dates(fn: str, directory: str = None) -> (datetime.date, datetime.date):
    """
    Extract start and end date of stock history from csv file
    :param fn: file name
    :param directory: directory name
    :return: start and end dates if found, otherwise None
    """
    path = get_path(fn, directory)
    line = "\n"

    try:
        with open(path, 'r') as file:
            while not line.startswith("History Period:"):
                line = file.readline()

                if not line:
                    return None

    except FileNotFoundError:
        return None
    except PermissionError:
        return None

    data = line.split(",")[0].strip().removeprefix("History Period: ").split(" - ")
    date_format = "%d-%b-%Y"
    start_date = datetime.strptime(data[0], date_format).date()
    end_date = datetime.strptime(data[0], date_format).date()

    return start_date, end_date


def csv_get_volume(fn: str, directory: str = None) -> int | None:
    """
    Extract company stock volume from csv file
    :param fn: file name
    :param directory: directory name
    :return: stock volume if found, otherwise None
    """
    path = get_path(fn, directory)
    line = "\n"

    try:
        with open(path, 'r') as file:
            while not line.startswith("VAP: Total"):
                line = file.readline()

                if not line:
                    return None

    except FileNotFoundError:
        return None
    except PermissionError:
        return None

    volume = "".join(line.split(",")[1:]).strip()
    volume = re.sub(r"[^0-9]", "", volume)

    return int(volume)


def csv_get_metadata(fn: str, directory: str = None) -> dict[str:str]:
    """
    Extracts a dictionary containing metadata that can be extracted from unformatted csv file
    :param fn: Name of file
    :param directory: Directory of file
    :return: dictionary containing metadata for data that was found, otherwise, value is None
    """
    # gets just file name
    path, fn, directory = get_path(fn, directory, get_fn_dir=True)

    comp_name = csv_get_comp_name(fn, directory)
    symbol = csv_get_symbol(fn, directory)
    start_date, end_date = csv_get_dates(fn, directory)
    volume = csv_get_volume(fn, directory)

    data = {
        'Symbol': symbol,
        'Company': comp_name,
        'Start_Date': start_date,
        'End_Date': end_date,
        'Volume': volume,
    }

    return data


def csv_get_all_metadata(directory: str) -> pd.DataFrame:
    """
    Extracts metadata from all files in a directory as pandas dataframe
    :param directory: directory to extract from
    :return: pandas dataframe
    """
    # completes operation on files in directory
    df = extract_all(csv_get_metadata, directory)
    return df