"""
This module is used to save and retrieve data from a database
"""

from .shared import get_path
from sqlalchemy import create_engine, exc
import pandas as pd
import os


def df_to_db(df: pd.DataFrame, db_name: str, table_name: str, directory: str = None) -> bool:
    """
    Saves a pandas dataframe to a table in a database
    :param df: Dataframe to store
    :param db_name: Name of database (automatically post-pends ".db")
    :param table_name: Name of table in database
    :param directory: Optionally, a directory to store database
    :return: True if successful, otherwise False
    """

    if not isinstance(df, pd.DataFrame):
        return False

    # if db name not ending in db, add db
    if not db_name.endswith('.db'):
        db_name += '.db'

    # ensure fn and path are seperated
    path, fn, directory = get_path(db_name, directory, True)

    # if directory does not yet exist, construct it
    os.makedirs(directory, exist_ok=True)

    # Create a SQLite database file in the specified directory
    try:
        engine = create_engine(f"sqlite:///{path}", echo=False)
    except exc.OperationalError:
        return False

    # write data to database
    with engine.begin() as connection:
        df.to_sql(name=table_name, con=connection, if_exists='replace', index=False)

    return True


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
    path = get_path(db_name, directory)

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