"""
This module is used to extract metadata from transcipts
"""
from ..shared.shared import find_index
import datetime
import re
import os


def get_metadata(
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
        date_format = r"%Y-%m-%d"

        date_line = date_line.upper()
        date = re.sub(date_re, "", date_line)
        if date == date_line():
            date = None
        else:
            date = date.strip()
            date = datetime.datetime.strptime(date, date_format)

        name_re = "\(.*\)"
        name = re.sub(name_re, "", name_symbol_line)
        if name == name_symbol_line:
            name = None
        else:
            name = name.strip().capitalize()

        
        symbol_re_list = ("^.*\(", "US Equity\)")
        for symbol_re in symbol_re_list:
            symbol = re.sub(symbol_re, "", name_symbol_line)
            if symbol == name_symbol_line:
                symbol = None
                break
        
        if symbol is not None:
            symbol = symbol.strip()

    except FileNotFoundError or PermissionError:
        date = None
        name = None
        symbol = None

    fn = os.path.basename(fn)
    fn_split = fn.removesuffix('.txt').split(' ')
    id = fn_split[-1]

    suffix_kws = ['Inc', 'Corp']
    start_idx = find_index(suffix_kws, fn_split)

    suffix_kws = ['Day', 'Call']
    end_idx = find_index(suffix_kws, fn_split)

    if start_idx is not None and end_idx is not None:
        conf = ' '.join(fn_split[(start_idx + 1):(end_idx + 1)])
    else:
        conf = None

    data = {
        'ID': id,
        'Symbol': symbol,
        'Company': name,
        'Date': date,
        'Type': conf,
    }

    return data