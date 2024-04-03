import pandas as pd
import os
from alive_progress import alive_bar
from .shared import merge_dicts
from ..file_helper import dir_exists


def format_all(
        format_func,
        title,
        src_ext: str,
        src_dir: str,
        dst_dir: str = None,
        sort_values: list[str] = None,
        overwrite: bool = False
) -> pd.DataFrame | None:
    """
    Formats all files by given format_func in src_dir and saves them in dst_dir
    :param format_func: format function to call on each file
    :param title: name of process
    :param src_ext: extension to call function on
    :param src_dir: Directory where files are currently stored
    :param dst_dir: Directory to store files
    :param sort_values: List of columns to sort by
    :param overwrite: Whether to overwrite all files or not
    :return: Pandas dataframe with all IDs and new file names
    """
    if dst_dir is None:
        dst_dir = src_dir + "_formatted"
    
    title = f'{title: <30}'

    if not dir_exists(src_dir):
        return None

    data = {}
    files = os.listdir(src_dir)
    with alive_bar(len(files), force_tty=True, title=title) as bar:
        for file in files:
            if not file.endswith(src_ext):
                bar()
                continue

            src_fn = os.path.join(src_dir, file)
            row_data = format_func(src_fn, dst_dir, overwrite)
            data = merge_dicts(data, row_data)
            bar()
    
    df = pd.DataFrame.from_dict(data)
    if sort_values is not None:
        df.sort_values(by=sort_values, ascending=True, inplace=True)
    return df