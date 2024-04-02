import os
import re
from ..shared import extract_all
import pandas as pd
import numpy as np

def earnings_metadata(
        fn: str
) -> dict[str: str | None]:
    """
    Extracts metadata from file name and contents
    :param fn: name of file to extract metadata from
    :return: dict containing found metadata
    """
    symbol = os.path.basename(fn).split(' ')[0]

    if len(symbol) > 4:
        symbol = symbol[:4]
    
    # Indicate type of earnings
    if 'EPS' in os.path.basename(fn).upper():
        e_type = 'EPS'
    elif 'REV' in os.path.basename(fn).upper():
        e_type = 'REV'
    else:
        e_type = np.NaN

    data = {
        'Symbol': symbol,
        'Type': e_type
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
    df = extract_all(earnings_metadata, '.txt', src_dir)
    return df