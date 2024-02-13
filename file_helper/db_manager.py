"""
This module is used to save and retrieve data from a database
"""

from .shared import ensure_fn_path
from sqlalchemy import create_engine
import pandas as pd
import os


def df_to_db(df: pd.DataFrame, db_name: str, table_name: str, directory: str = None) -> None:
    """
    Saves a pandas dataframe to a table in a database
    :param df: Dataframe to store
    :param db_name: Name of database (automatically post-pends ".db")
    :param table_name: Name of table in database
    :param directory: Optionally, a directory to store database
    :return: None
    """
    # if db name not ending in db, add db
    if not db_name.endswith('.db'):
        db_name += '.db'

    # ensure fn and path are seperated
    path, db_name, directory = ensure_fn_path(db_name, directory)

    # if directory does not yet exist, construct it
    if directory is not None:
        os.makedirs(directory, exist_ok=True)

    # Create a SQLite database file in the specified directory
    engine = create_engine(f"sqlite:///{path}", echo=False)

    # write data to database
    with engine.begin() as connection:
        df.to_sql(name=table_name, con=connection, if_exists='replace', index=False)


def db_to_df(db_name: str, table_name: str, directory: str = None) -> pd.DataFrame | None:
    """
    Extracts a table from a database as a pandas dataframe
    :param db_name: Name of database (automatically post-pends ".db")
    :param table_name: Name of table in database
    :param directory: Optionally, a directory to store database
    :return: Pandas Dataframe if exists, otherwise None
    """
    # if db name not ending in db, add db
    if not db_name.endswith('.db'):
        db_name += '.db'

    # ensure fn and path are seperated
    path, db_name, directory = ensure_fn_path(db_name, directory)

    # attempts to create connection to table
    # fails if database doesn't exist
    try:
        engine = create_engine(f"sqlite:///{path}", echo=False)
    except FileNotFoundError:
        return None

    # queries table for all data
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, engine)

    return df