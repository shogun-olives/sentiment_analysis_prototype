from shared import file_exists, not_existing_files
import os
import pandas as pd
from alive_progress import alive_bar


def xlsx_to_csv(xlsx_fn: str, csv_fn: str, overwrite: bool = False) -> bool:
    """
    Reads in a xlsx file and writes it to a csv file
    :param xlsx_fn: name of xlsx file to read
    :param csv_fn: name of file to write
    :param overwrite: True to overwrite all existing files, False to overwrite none, leave None for user prompt
    :return: True if process succeeded, otherwise False
    """
    if not xlsx_fn.endswith('.xlsx'):
        return False
    if not csv_fn.endswith('.csv'):
        csv_fn += '.csv'

    if file_exists(csv_fn) and not overwrite:
        return False

    try:
        xlsx_fn = os.path.abspath(xlsx_fn)
        csv_fn = os.path.abspath(csv_fn)
        df = pd.read_excel(xlsx_fn)
    except FileNotFoundError:
        return False

    os.makedirs(os.path.dirname(csv_fn), exist_ok=True)
    df.to_csv(csv_fn, index=False)
    return True


def all_xlsx_to_csv(src_dir: str, dst_dir: str = None, overwrite: bool = False) -> None:
    """
    Takes all xlsx files in directory and converts them to csv files in target_directory
    :param src_dir: Directory with xlsx files
    :param dst_dir: Directory to store txt files in (defaults to directory\\txt)
    :param overwrite: True to replace all, False to replace nothing
    :return: None
    """
    try:
        src_dir = os.path.abspath(src_dir)
        if dst_dir is None:
            dest = os.path.join(os.path.dirname(src_dir), 'txt')
        else:
            dst_dir = os.path.abspath(dst_dir)
        files = os.listdir(src_dir)
    except FileNotFoundError or OSError:
        return None

    # gets list of file names that already exist in target directory and corresponding new name
    csv_files = [file.removesuffix('.xlsx') + '.csv' for file in files if file.endswith('.xlsx')]

    if not file_exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)
    elif not overwrite:
        csv_files = not_existing_files(csv_files, dst_dir)

    with alive_bar(len(csv_files), force_tty=True, title='Converting .xlsx to .csv') as bar:
        for file in csv_files:
            src_file = os.path.join(src_dir, file.removesuffix('.csv') + '.xlsx')
            dst_file = os.path.join(dst_dir, file)
            xlsx_to_csv(src_file, dst_file)
            bar()

    return None


def main() -> None:
    # xlsx = r"..\raw\earnings\xlsx\AAPL EPS.xlsx"
    # csv = r"..\raw\earnings\csv\AAPL EPS.csv"
    # print(xlsx_to_csv(xlsx, csv))
    all_xlsx_to_csv('../raw/earnings/xlsx', '../raw/earnings/csv')
    pass


if __name__ == "__main__":
    main()