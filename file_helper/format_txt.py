import pandas as pd
import re
import os
import timeit


def file_exists(fn) -> bool:
    # checks if file exists
    if not os.path.exists(fn):
        return False

    # checks if file has data
    if os.path.getsize(fn) == 0:
        return False

    # if file doesn't exist or has no data, return true
    return True


def get_symbol(fn: str) -> str | None:
    with open(fn, 'r', encoding='utf-8') as file:
        for _ in range(2):
            line = file.readline()
        words = line.split(' ')
        for word in words:
            if '(' in word:
                word = word.removeprefix('(')
                if len(word) > 4:
                    word = word[:4]
                return word
    return None


def format_title(fn: str) -> str:
    symbol = get_symbol(fn)

    fn = os.path.basename(fn)
    words = fn.removesuffix('.txt').split(' ')

    date = words[-2]
    date = f'{(lambda x: '0'+x if len(x) < 2 else x)(date[4:-2])}.{date[-2:]}.{date[:4]}'

    conf_id = words[-1]

    return f'{symbol}_{date}_{conf_id}.txt'


def clean_text(rgx_list: list[str], text: str) -> str:
    new_text = text
    for rgx_match in rgx_list:
        new_text = re.sub(rgx_match, '', new_text)
    return new_text


def format_txt(fn: str, dest: str, overwrite: bool = False) -> dict[str:str]:
    id_key = os.path.basename(fn).removesuffix('.txt').split(' ')[-1]

    new_fn = format_title(fn)
    dest = os.path.abspath(dest)
    new_path = os.path.join(dest, new_fn)

    data = {
        'ID': [id_key],
        'File': [new_fn]
    }

    if file_exists(new_path) and not overwrite:
        return data

    try:
        with open(fn, 'r', encoding='utf-8') as file:
            contents = file.read()
    except OSError:
        return None

    beginning = re.compile(r'^.*?}', re.DOTALL)
    contents = re.sub(beginning, '', contents)

    page_mark = re.compile(fr'{re.escape('FINAL TRANSCRIPT')}.*?{re.escape('of')} [0-9]+', re.DOTALL)
    contents = re.sub(page_mark, '\n', contents)

    bio_mark = r'{(.*?)}'
    contents = re.sub(bio_mark, '', contents)

    ending = re.compile(r'This transcript may not be 100 percent accurate.*$', re.DOTALL)
    contents = re.sub(ending, '', contents)

    mapping = {
        'ﬁ': 'fi',
        'ﬀ': 'ff',
    }
    translation_table = str.maketrans(mapping)
    contents = contents.translate(translation_table)

    os.makedirs(dest, exist_ok=True)

    with open(new_path, 'w', encoding='utf-8') as file:
        file.write(contents.strip())

    return data


def format_all_txt(curr: str, dest: str, overwrite: bool = False) -> pd.DataFrame:
    data = []

    # overwrites all files that are not marked to keep
    count = 0
    delim = '\t\t'
    t0 = timeit.default_timer()
    for file in os.listdir(curr):
        t1 = timeit.default_timer()
        exists = file_exists(os.path.join(curr, file))
        row = format_txt(os.path.join(curr, file), dest, overwrite)

        data.append(pd.DataFrame.from_dict(row))

        if row is None:
            continue

        count += 1
        if count >= 100:
            delim = '\t'

        t2 = timeit.default_timer()
        if overwrite:
            print(f"{count}.{delim}[{row['File'][0]}] written in {t2 - t1} sec")
        elif not exists:
            print(f"{count}.{delim}[{row['File'][0]}] written in {t2 - t1} sec")

    t3 = timeit.default_timer()
    if overwrite:
        print(f'\nOperation completed in {t3 - t0:.2f} seconds')

    df = pd.concat(data, ignore_index=True)

    return df