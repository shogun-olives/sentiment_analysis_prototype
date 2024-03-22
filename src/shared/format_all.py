import pandas as pd
import os
from alive_progress import alive_bar
from .shared import merge_dicts


def format_all(
        format_func,
        title,
        src_ext: str,
        src_dir: str,
        dst_dir: str = None,
        overwrite: bool = False
    ) -> pd.DataFrame | None:
    """
    Formats all files by given format_func in src_dir and saves them in dst_dir
    :param format_func: format function to call on each file
    :param title: name of process
    :param src_ext: extension to call function on
    :param src_dir: Directory where files are currently stored
    :param dst_dir: Directory to store files
    :param overwrite: Whether to overwrite all files or not
    :return: Pandas dataframe with all IDs and new file names
    """
    src_dir = os.path.abspath(src_dir)
    if dst_dir is None:
        dst_dir = src_dir + "_formatted"
    else:
        dst_dir = os.path.abspath(dst_dir)
    
    data = {}
    files = os.listdir(src_dir)
    with alive_bar(len(files), force_tty=True, title=title) as bar:
        for file in files:
            if not file.endswith(src_ext):
                bar()
                continue

            row_data = format_func(os.path.join(src_dir, file), dst_dir, overwrite)
            data = merge_dicts(data, row_data)
            bar()
    
    df = pd.DataFrame.from_dict(data)
    return df