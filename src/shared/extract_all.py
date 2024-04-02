import os
from ..file_helper import dir_exists
from .shared import merge_dicts
import pandas as pd


def extract_all(
        func,
        src_ext: str,
        src_dir: str
) -> pd.DataFrame | None:
    """
    calls func on every file in directory and returns a dataframe containing all data extracted this way
    :param func: a function to be called on every file in a directory returning a dict of data
    :param src_ext: extension type of file to open
    :param src_dir: directory to extract from
    :return: pandas dataframe if no error, otherwise None
    """
    data = {}

    if not dir_exists(src_dir):
        return None

    for file in os.listdir(src_dir):
        if not file.endswith(src_ext):
            continue

        src_fn = os.path.join(file, src_dir)
        row_data = func(src_fn)
        data = merge_dicts(data, row_data)

    df = pd.DataFrame.from_dict(data)
    df.sort_values(by=['Symbol', 'Date'], ascending=True, inplace=True)
    return df