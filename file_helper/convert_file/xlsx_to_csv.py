"""
Convert xlsx to csv
"""
import pandas as pd
import os
from ..check_file import file_exists
from .convert_all import convert_all


def rapid_xlsx_to_csv(
        xlsx_path: str,
        csv_path: str
    ) -> bool:
    """
    Abbreviated version where sanity checks are skipped\n
    Reads in a xlsx file and writes it to a csv file
    :param xlsx_path: path to xlsx file to read
    :param csv_path: path to file to write
    :return: True if process succeeded, otherwise False
    """    
    try:
        df = pd.read_excel(xlsx_path)
    except FileNotFoundError:
        return False

    df.to_csv(csv_path, index=False)
    return True


def xlsx_to_csv(xlsx_fn: str, csv_fn: str, overwrite: bool = False) -> bool:
    """
    Reads in a xlsx file and writes it to a csv file
    :param xlsx_fn: name of xlsx file to read
    :param csv_fn: name of file to write
    :param overwrite: True to overwrite file, False to skip
    :return: True if process succeeded, otherwise False
    """
    xlsx_fn = os.path.abspath(xlsx_fn)
    csv_fn = os.path.abspath(csv_fn)
    
    # exception handling for extensions
    if not xlsx_fn.endswith('.xlsx') or not csv_fn.endswith('.csv'):
        return False
    
    if file_exists(csv_fn) and not overwrite:
        return False
    
    try:
        df = pd.read_excel(xlsx_fn)
    except FileNotFoundError:
        return False

    os.makedirs(os.path.dirname(csv_fn), exist_ok=True)
    df.to_csv(csv_fn, index=False)
    return True


def all_xlsx_to_csv(
        src_dir: str,
        dst_dir: str = None,
        overwrite: bool = False
    ) -> None:
    """
    Converts all xlsx files in src_dir to csv files in dst_dir
    :param src_dir: Directory with xlsx files
    :param dst_dir: Directory to store csv files ([src_dir]_csv)
    :param overwrite: True to replace all, False to replace none
    :return: None
    """
    convert_all(
        rapid_xlsx_to_csv,
        '.xlsx', '.csv',
        src_dir, dst_dir,
        overwrite
    )

    return None