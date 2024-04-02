"""
This module takes an unformatted csv file and formats it for sentiment analysis
"""
from ..shared.format_all import format_all
from .stock_metadata import stock_metadata
from ..file_helper.check_file import file_exists
import pandas as pd
import os
from datetime import datetime


def new_fn(
        fn: str
) -> str:
    """
    Takes a file and returns an abbreviated file name
    :param fn: Relative or Absolute path to old file
    :return: new base name of file only
    """
    fn = os.path.abspath(fn)
    data = stock_metadata(fn)

    symbol = data['Symbol']
    date = data['End_Date']

    if any(item is None for item in (symbol, date)):
        return fn

    return f'{symbol}_{date}.csv'


def format_stock(
        src_fn: str,
        dst_dir: str,
        overwrite: bool = False
) -> dict[str:str]:
    """
    Formats a stock csv file for sentiment analysis
    :param src_fn: name of unformatted file
    :param dst_dir: name of directory to save new file at
    :param overwrite: True to overwrite existing, False to do nothing
    :return: dictionary containing stock metadata
    """
    src_fn = os.path.abspath(src_fn)

    if dst_dir is None:
        dst_dir = os.path.dirname(src_fn)
    
    dst_fn = os.path.join(dst_dir, new_fn(src_fn))

    data = stock_metadata(src_fn)
    data['File'] = os.path.basename(dst_fn)

    os.makedirs(dst_dir, exist_ok=True)

    if file_exists(dst_fn) and not overwrite:
        return data

    line = "\n"
    data_start = "Exchange Date,Close,Net,%Chg,Open,Low,High,Volume,Turnover - USD,Flow,,,,,,\n"

    try:
        with open(src_fn, 'r') as src_file:
            while line != data_start:
                line = src_file.readline()
                if not line:
                    return None

            with open(dst_fn, 'w') as dst_file:
                dst_file.write(data_start.strip().rstrip(",") + "\n")
                while line:
                    line = src_file.readline()
                    line_data = (line.strip().rstrip(",") + "\n").split(",")
                    if len(line_data) > 3:
                        line_data[0] = str(datetime.strptime(line_data[0], "%d-%b-%Y").date())
                    dst_file.write(','.join(line_data))
    except FileNotFoundError:
        return None

    return data


def format_all_stocks(
        src_dir: str,
        dst_dir: str = None,
        overwrite: bool = False
) -> pd.DataFrame:
    """
    Formats all stock csv files in src_dir and saves them in dst_dir
    :param src_dir: Directory with transcript txts
    :param dst_dir: Directory to store formatted txts
    :param overwrite: Whether to overwrite all files or not
    :return: Pandas dataframe with all IDs and new file names
    """
    df = format_all(
        format_stock,
        "Formatting Stocks",
        ".csv",
        src_dir, dst_dir,
        ["Symbol"],
        overwrite
    )
    return df