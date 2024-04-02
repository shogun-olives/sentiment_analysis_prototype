"""
This module formats transcipts to be analyzed for sentiment
"""
from ..shared import format_all
from .transcript_metadata import transcript_metadata
from ..file_helper.check_file import file_exists
import pandas as pd
import re
import os


def new_fn(
        fn: str
) -> str:
    """
    Takes a file and returns an abbreviated file name
    :param fn: Relative or Absolute path to old file
    :return: new base name of file only
    """
    fn = os.path.abspath(fn)
    data = transcript_metadata(fn)

    symbol = data['Symbol']
    date = data['Date']
    uid = data['ID']

    if any(item is None for item in (symbol, date, uid)):
        return fn

    return f'{symbol}_{date}_{uid}.txt'


def format_transcript(
        src_fn: str, 
        dst_dir: str = None,
        overwrite: bool = False
) -> dict[str:str]:
    """
    Formats a transcript txt file for sentiment analysis
    :param src_fn: name of unformatted file
    :param dst_dir: name of directory to save new file at
    :param overwrite: True to overwrite existing, False to do nothing
    :return: dictionary containing transcript metadata
    """
    src_fn = os.path.abspath(src_fn)

    if dst_dir is None:
        dst_dir = os.path.dirname(src_fn)
    
    dst_fn = os.path.join(dst_dir, new_fn(src_fn))

    data = transcript_metadata(src_fn)
    data['File'] = os.path.basename(dst_fn)

    if file_exists(dst_fn) and not overwrite:
        return data

    try:
        with open(src_fn, 'r', encoding='utf-8') as file:
            contents = file.read()
    except OSError:
        return None

    # remove pretext from file
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

    os.makedirs(dst_dir, exist_ok=True)
    with open(dst_fn, 'w', encoding='utf-8') as file:
        file.write(contents.strip())

    return data


def format_all_transcripts(
        src_dir: str,
        dst_dir: str = None,
        overwrite: bool = False
) -> pd.DataFrame:
    """
    Formats all tramscript txt files in src_dir and saves them in dst_dir
    :param src_dir: Directory with transcript txts
    :param dst_dir: Directory to store formatted txts
    :param overwrite: Whether to overwrite all files or not
    :return: Pandas dataframe with all IDs and new file names
    """
    df = format_all(
        format_transcript,
        "Formatting Transcripts",
        ".txt",
        src_dir, dst_dir,
        ['Symbol', 'Date'],
        overwrite
    )
    return df