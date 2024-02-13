"""
This module takes an unformatted text file and formats it for sentiment analysis
"""
from .shared import file_exists, get_symbol, date_from_fn, id_from_fn, ensure_fn_path
import pandas as pd
import re
import os
import timeit


def format_title(fn: str, directory: str = None) -> str:
    """
    Takes a filename and directory and extracts an abbreviated file name
    :param fn: Name of file
    :param directory: Name of directory
    :return: new file name
    """
    path, fn, directory = ensure_fn_path(fn, directory)

    symbol = get_symbol(fn, directory)
    date = date_from_fn(fn)
    conf_id = id_from_fn(fn)

    return f'{symbol}_{date}_{conf_id}.txt'


def format_txt(fn: str, dest: str, curr: str = None, overwrite: bool = False) -> dict[str:str]:
    """
    Takes unformatted txt file and formats it for sentiment analysis
    :param fn: name of file
    :param dest: name of directory to save new file at
    :param curr: name of directory to read file from
    :param overwrite: True to overwrite existing, False to do nothing
    :return: dictionary containing ID and new name
    """
    # get new file name
    new_fn = format_title(fn, curr)

    # determine absolute path to destination directory
    curr_path, curr_fn, curr_directory = ensure_fn_path(fn, curr)
    dest_path, dest_fn, dest_directory = ensure_fn_path(new_fn, dest)

    # create array storing data
    data = {
        'ID': [id_from_fn(curr_fn)],
        'File': ['.\\' + os.path.relpath(dest_path, os.getcwd())]
    }

    # if file already exists, and overwrite is false, don't overwrite
    if file_exists(dest_path) and not overwrite:
        return data

    # open old file
    try:
        with open(curr_path, 'r', encoding='utf-8') as file:
            contents = file.read()
    except OSError:
        return None

    # remove starting text from file
    beginning = re.compile(r'^.*?}', re.DOTALL)
    contents = re.sub(beginning, '', contents)

    # remove page numbers from file
    page_mark = re.compile(fr'{re.escape('FINAL TRANSCRIPT')}.*?{re.escape('of')} [0-9]+', re.DOTALL)
    contents = re.sub(page_mark, '\n', contents)

    # remove {bio...} from file
    bio_mark = r'{(.*?)}'
    contents = re.sub(bio_mark, '', contents)

    # remove ending disclaimer from file
    ending = re.compile(r'This transcript may not be 100 percent accurate.*$', re.DOTALL)
    contents = re.sub(ending, '', contents)

    # replace unmapped characters with normal characters
    mapping = {
        'ﬁ': 'fi',
        'ﬀ': 'ff',
    }
    translation_table = str.maketrans(mapping)
    contents = contents.translate(translation_table)

    # creates directory to file if it doesn't exist
    os.makedirs(dest_directory, exist_ok=True)

    # writes data to file
    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(contents.strip())

    # return dict
    return data


def format_all_txt(curr: str, dest: str, overwrite: bool = False, display_progress: bool = False) -> pd.DataFrame:
    """
    Formats all files in curr directory and saves them in dest directory
    :param curr: Directory where files are currently stored
    :param dest: Directory to store files
    :param overwrite: Whether to overwrite all files or not
    :param display_progress: Display time to complete operation
    :return: Pandas dataframe with all IDs and new file names
    """
    # empty list to put data in
    data = []

    # counters
    count = 0
    t0 = timeit.default_timer()

    if display_progress:
        print('Writing:')

    # iterates through each file to rewrite
    for file in os.listdir(curr):
        # times operation
        t1 = timeit.default_timer()

        # writes data
        row = format_txt(file, dest, curr, overwrite)

        # only keeps track of files that were successfully written
        if row is None:
            continue

        # appends data to dataframe
        data.append(pd.DataFrame.from_dict(row))
        t2 = timeit.default_timer()

        # displays progress
        if display_progress:
            print(f"\t{count}.\t[{row['File'][0]}] written in {t2 - t1} sec")

    # times entire operation
    t3 = timeit.default_timer()
    if display_progress:
        print(f'\nOperation completed in {t3 - t0:.2f} seconds')

    # concatenates all data into one dataframe
    df = pd.concat(data, ignore_index=True)

    return df