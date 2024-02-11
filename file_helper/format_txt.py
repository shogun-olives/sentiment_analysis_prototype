import os
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

    call_index = find_index(corp_suffixes, words) + 1
    date_index = words.index('Call') + 1

    company_name = ' '.join(words[:call_index])
    presentation_type = ' '.join(words[call_index:date_index])
    presentation_id = words[-1]

    return presentation_id, company_name, presentation_type


def get_symbol(line: str) -> str | None:
    words = line.split(' ')
    for word in words:
        if '(' in word:
            return word.removeprefix('(')
    return None


def get_data(fn) -> dict[str: str]:
    presentation_id, company_name, presentation_type = extract_from_title(fn)

    with open(fn, 'r', encoding='utf-8') as file:
        line = file.readline().removeprefix('FINAL TRANSCRIPT').strip()
        date = datetime.strptime(line, '%Y-%m-%d').date()

        line = file.readline()
        symbol = get_symbol(line)

    data = {
        'ID': presentation_id,
        'Company': company_name,
        'Symbol': symbol,
        'Date': date,
        'Type': presentation_type,
        'File': fn
    }

    return data


def main() -> None:
    get_data('../raw_files/transcripts/txt/Alphabet Inc Conf Presentation Call 2015304 FS000000002197545639.txt', '')
    pass


if __name__ == '__main__':
    main()