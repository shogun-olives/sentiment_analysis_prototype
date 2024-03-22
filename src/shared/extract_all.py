import os
import pandas as pd

def extract_all(func, directory: str) -> pd.DataFrame | None:
    """
    calls func on every file in directory and returns a dataframe containing all data extracted this way
    :param func: a function to be called on every file in a directory returning a dict of data
    :param directory: directory to extract from
    :return: pandas dataframe if no error, otherwise None
    """
    # empty array to store data
    data = []

    # for each file, try to extract metadata
    for file in os.listdir(directory):
        row = func(file, directory)

        if row is None:
            continue

        # ensures every val in dict is list for concatenation
        for key in row:
            if not isinstance(row[key], list):
                row[key] = [row[key]]

        # adds row to data
        data.append(pd.DataFrame.from_dict(row))

    # concatenate all data into a dataframe
    df = pd.concat(data, ignore_index=True)
    return df