import os
from io import StringIO
from .earnings_metadata import earnings_metadata
from ..file_helper import file_exists
from ..shared import format_all
import pandas as pd


def new_fn(
        fn: str
) -> str:
    """
    Takes a file and returns an abbreviated file name
    :param fn: Relative or Absolute path to old file
    :return: new base name of file only
    """
    fn = os.path.abspath(fn)
    data = earnings_metadata(fn)

    symbol = data['Symbol']
    s_type = data['Type']

    if any(item is None for item in (symbol, s_type)):
        return fn

    return f'{symbol}_{s_type}.txt'


def format_earnings(
    src_fn: str,
    dst_dir: str = None,
    overwrite: bool = False
) -> dict[str:str]:
    
    src_fn = os.path.abspath(src_fn)

    if dst_dir is None:
        dst_dir = os.path.dirname(src_fn)
    
    dst_fn = os.path.join(dst_dir, new_fn(src_fn))

    metadata = earnings_metadata(src_fn)
    metadata['File'] = os.path.basename(dst_fn)

    if file_exists(dst_fn) and not overwrite:
        return metadata
    
    with open(src_fn, 'r') as file:
        data = file.read()

    # Remove misc data
    match_str = 'Average of Absolute Values'
    data = StringIO('\n'.join([line.strip() for line in data.split('\n') if match_str not in line]))
    df = pd.read_table(data, sep=",")

    # Only keep columns of interest
    df = df[['Ann Date', 'Per', 'Per End', 'Reported', 'Estimate', '%Surp']]
    df.rename(columns={"Ann Date": "Date"}, inplace=True)
    
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['Per End'] = pd.to_datetime(df['Per End'], format='%m/%d')

    # Add if expectations were beat or not
    df['Beat Pred'] = pd.to_numeric(df['%Surp'].str.removesuffix('%'), errors='coerce').apply(lambda x: 1 if x > 0 else 0)

    # save to file
    os.makedirs(dst_dir, exist_ok=True)
    df.to_csv(dst_fn, index=False)
    return metadata


def format_all_earnings(
    src_dir: str,
    dst_dir: str,
    overwrite: bool = False
) -> pd.DataFrame:
    df = format_all(
        format_earnings,
        "Formatting Earnings",
        ".csv",
        src_dir, dst_dir,
        'Symbol',
        overwrite
    )
    return df