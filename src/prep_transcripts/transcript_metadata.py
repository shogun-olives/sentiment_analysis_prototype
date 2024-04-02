"""
This module is used to extract metadata from transcripts
"""
from ..shared import find_index, extract_all
import pandas as pd
import re
import os


def transcript_metadata(
        fn: str
) -> dict[str: str | None]:
    """
    Extracts metadata from file name and contents
    :param fn: name of file to extract metadata from
    :return: dict containing found metadata
    """
    fn = os.path.abspath(fn)

    try:
        with open(fn, 'r', encoding='utf-8') as file:
            date_line = file.readline()
            name_symbol_line = file.readline().strip()
        
        date_re = "^FINAL TRANSCRIPT"

        date_line = date_line.upper()
        date = re.sub(date_re, "", date_line)
        if date == date_line:
            date = None
        else:
            date = date.strip()

        name_re = r"\(.*\)"
        name = re.sub(name_re, "", name_symbol_line)
        if name == name_symbol_line:
            name = None
        else:
            name = name.strip().capitalize()

        symbol_re = r'\(.*?Equity\)'
        symbol = re.findall(symbol_re, name_symbol_line)[0]
        if symbol == name_symbol_line:
            symbol = None
        else:
            symbol = symbol.removeprefix('(').removesuffix('US Equity)').strip()
            if len(symbol) > 4:
                symbol = symbol[:4]

    except FileNotFoundError or PermissionError:
        date = None
        name = None
        symbol = None

    fn = os.path.basename(fn)
    fn_split = fn.removesuffix('.txt').split(' ')
    uid = fn_split[-1]

    suffix_kws = ['Inc', 'Corp']
    start_idx = find_index(fn_split, suffix_kws)

    suffix_kws = ['Day', 'Call']
    end_idx = find_index(fn_split, suffix_kws)

    if start_idx is not None and end_idx is not None:
        conf = ' '.join(fn_split[(start_idx + 1):(end_idx + 1)])
    else:
        conf = None

    data = {
        'ID': uid,
        'Symbol': symbol,
        'Company': name,
        'Date': date,
        'Type': conf,
    }

    return data


def all_transcript_metadata(
        src_dir: str
) -> pd.DataFrame:
    """
    Gets transcript metadata from all transcripts in src_dir
    :param src_dir: directory to extract data from
    :return: pandas dataframe with all data
    """
    df = extract_all(transcript_metadata, '.txt', src_dir)
    return df