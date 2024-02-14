"""
This module takes an unformatted text file and formats it for sentiment analysis
"""
from .shared import file_exists, get_path, format_all
from .txt_metadata import txt_get_symbol, txt_get_date, txt_get_id
import pandas as pd
import re
import os


def format_title(fn: str, directory: str = None) -> str:
    """
    Takes a filename and directory and extracts an abbreviated file name
    :param fn: Name of file
    :param directory: Name of directory
    :return: new file name
    """
    path, fn, directory = get_path(fn, directory, True)

    symbol = txt_get_symbol(fn, directory)
    date = txt_get_date(fn)
    conf_id = txt_get_id(fn)

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
    curr_path, curr_fn, curr_directory = get_path(fn, curr, True)
    dest_path, dest_fn, dest_directory = get_path(new_fn, dest, True)

    # create array storing data
    data = {
        'ID': [txt_get_id(curr_fn)],
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
    # runs template on given function
    df = format_all(format_txt, ".txt", curr, dest, overwrite, display_progress)
    return df