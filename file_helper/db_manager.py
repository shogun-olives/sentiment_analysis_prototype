from sqlalchemy import create_engine
import pandas as pd
import os


def df_to_db(df, db_name: str, table_name: str, path: str = None) -> None:
    # If path and name given, set name as path and name
    if path is not None:
        db_name = os.path.join(path, db_name)

    # if db name not ending in db, add db
    if not db_name.endswith('.db'):
        db_name += '.db'

    # Create a SQLite database file in the specified directory
    engine = create_engine(f"sqlite:///{db_name}", echo=False)

    # write data to database
    with engine.begin() as connection:
        df.to_sql(name=table_name, con=connection, if_exists='append')


def db_to_df(db_name: str, table_name: str, path: str = None) -> pd.DataFrame:
    # If path and name given, set name as path and name
    if path is not None:
        db_name = os.path.join(path, db_name)

    # if db name not ending in db, add db
    if not db_name.endswith('.db'):
        db_name += '.db'

    # create connection and retrieve data
    engine = create_engine(f"sqlite:///{db_name}", echo=False)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, engine)

    return df

