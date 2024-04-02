"""
This module is used to save and retrieve data from a database
"""
from sqlalchemy import create_engine, exc
import pandas as pd
import os


def df_to_db(
        df: pd.DataFrame,
        db: str,
        table_name: str
) -> bool:
    """
    Saves a pandas dataframe to a table in a database
    :param df: Dataframe to store
    :param db: relative or absolute path to database
    :param table_name: Name of table in database
    :return: True if successful, otherwise False
    """
    if not db.endswith('.db'):
        return False

    db = os.path.abspath(db)
    os.makedirs(os.path.dirname(db), exist_ok=True)

    try:
        engine = create_engine(f"sqlite:///{db}", echo=False)
    except exc.OperationalError:
        return False

    with engine.begin() as connection:
        df.to_sql(name=table_name, con=connection, if_exists='replace', index=False)

    return True


def db_to_df(
        db: str,
        table_name: str
) -> pd.DataFrame | None:
    """
    Extracts a table from a database as a pandas dataframe
    :param db: Name of database (automatically post-pends ".db")
    :param table_name: Name of table in database
    :return: Pandas Dataframe if exists, otherwise None
    """
    if not db.endswith('.db'):
        return False
    
    db = os.path.abspath(db)

    try:
        engine = create_engine(f"sqlite:///{db}", echo=False)
    except FileNotFoundError:
        return None

    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, engine)
    return df