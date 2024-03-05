"""
This module takes an unformatted csv file and formats it for sentiment analysis
"""
from .shared import file_exists, get_path, format_all
from .csv_metadata import csv_get_symbol, csv_get_dates, csv_get_comp_name
import pandas as pd
import os
from datetime import datetime


def format_title(fn: str, directory: str = None) -> str:
    """
    Takes a csv file and formats its name
    :param fn: Name of file
    :param directory: Name of directory
    :return: new file name
    """
    path, fn, directory = get_path(fn, directory, True)

    symbol = csv_get_symbol(fn, directory)
    start_date, end_date = csv_get_dates(fn, directory)

    return f'{symbol}_{end_date}.csv'


def format_csv(fn: str, dest: str, curr: str = None, overwrite: bool = False) -> dict[str:str]:
    """
    Takes unformatted csv file and formats it for stock analysis
    :param fn: name of file
    :param dest: name of directory to save new file at
    :param curr: name of directory to read file from
    :param overwrite: True to overwrite existing, False to do nothing
    :return: dictionary containing symbol and new name
    """
    # get new file name
    new_fn = format_title(fn, curr)

    # determine absolute path to destination directory
    curr_path, curr_fn, curr_directory = get_path(fn, curr, True)
    dest_path, dest_fn, dest_directory = get_path(new_fn, dest, True)

    # create array storing data
    data = {
        'Company': [csv_get_comp_name(curr_fn, curr_directory)],
        'File': ['.\\' + os.path.relpath(dest_path, os.getcwd())]
    }

    # creates directory to file if it doesn't exist
    os.makedirs(dest_directory, exist_ok=True)

    if file_exists(dest_fn, dest_directory):
        if overwrite:
            pass
        else:
            return data

    line = "\n"
    data_start = "Exchange Date,Close,Net,%Chg,Open,Low,High,Volume,Turnover - USD,Flow,,,,,,\n"

    try:
        with open(curr_path, 'r') as curr_file:
            while line != data_start:
                line = curr_file.readline()
                if not line:
                    return None

            with open(dest_path, 'w') as dest_file:
                dest_file.write(data_start.strip().rstrip(",") + "\n")
                while line:
                    line = curr_file.readline()
                    line_data = (line.strip().rstrip(",") + "\n").split(",")
                    if len(line_data) > 3:
                        line_data[0] = str(datetime.strptime(line_data[0], "%d-%b-%Y").date())
                    dest_file.write(','.join(line_data))
    except FileNotFoundError:
        return None

    # return dict
    return data


def delete_row(fn: str, rows: int | str | list[int | str]) -> bool:
    if isinstance(rows, int) or rows.isdigit():
        lines = [int(rows)]
    elif isinstance(rows, list):
        lines = set(rows)
        lines = [int(row) for row in lines if isinstance(row, int) or row.isdigit()]
        lines = lines.sort()
    else:
        return False

    with open(fn, 'r+') as file:
        file_lines = file.readlines()
        file.seek(0)
        file.truncate()

        for line_num, line in enumerate(file_lines):
            if line_num not in lines:
                file.write(line)

    return True


def conditional_delete_row(fn: str, match: str) -> bool:
    with open(fn, 'r+') as file:
        file_lines = file.readlines()
        file.seek(0)
        file.truncate()

        match = match.strip()
        for line_num, line in enumerate(file_lines):
            if line.strip() == match:
                continue
            file.write(line)

    return True


def format_all_csv(curr: str, dest: str, overwrite: bool = False, display_progress: bool = False) -> pd.DataFrame:
    """
    Formats all files in curr directory and saves them in dest directory
    :param curr: Directory where files are currently stored
    :param dest: Directory to store files
    :param overwrite: Whether to overwrite all files or not
    :param display_progress: Display time to complete operation
    :return: Pandas dataframe with all IDs and new file names
    """
    # runs template on given function
    df = format_all(format_csv, ".csv", curr, dest, overwrite, display_progress)
    return df