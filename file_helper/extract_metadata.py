"""
This module is used to maneuver data between databases and dataframes
"""

import os
import pandas as pd
from datetime import datetime


def find_index(search: list[str], arr: list[str]) -> int | None:
    for word in search:
        try:
            index = arr.index(word)
            return index
        except ValueError:
            pass
    return None


def extract_from_title(fn: str) -> (str, str, str):
    fn = os.path.basename(fn)
    words = fn.removesuffix('.txt').split(' ')

    corp_suffixes = ['Inc', 'Corp']
    call_suffixes = ['Day', 'Call']

    try:
        call_index = find_index(corp_suffixes, words) + 1
        date_index = find_index(call_suffixes, words) + 1

        company_name = ' '.join(words[:call_index])
        conf_type = ' '.join(words[call_index:date_index])
        conf_id = words[-1]

        return conf_id, company_name, conf_type
    except TypeError:
        pass
    except IndexError:
        pass
    except ValueError:
        pass

    print(f'[{fn}] format invalid')
    return None, None, None


def get_symbol(line: str) -> str | None:
    words = line.split(' ')
    for word in words:
        if '(' in word:
            return word.removeprefix('(')
    return None


def get_metadata(fn) -> dict[str: str]:
    conf_id, company_name, conf_type = extract_from_title(fn)

    if any([x is None for x in (conf_id, company_name, conf_type)]):
        return None

    with open(fn, 'r', encoding='utf-8') as file:
        line = file.readline().split(' ')[-1].strip()
        date = datetime.strptime(line, '%Y-%m-%d').date()

        line = file.readline()
        symbol = get_symbol(line)

    data = {
        'ID': [conf_id],
        'Company': [company_name],
        'Symbol': [symbol],
        'Date': [date],
        'Type': [conf_type],
    }

    return data


def get_metadata_df(dir_name: str) -> pd.DataFrame:
    data = []
    for file in os.listdir(dir_name):
        row = get_metadata(os.path.join(dir_name, file))

        if row is None:
            continue

        data.append(pd.DataFrame.from_dict(row))

    df = pd.concat(data)

    return df