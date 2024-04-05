from ..file_helper import db_to_df
import pandas as pd
import os


def get_data(
    row: pd.Series,
    eps_df: pd.DataFrame,
    rev_df: pd.DataFrame
) -> pd.DataFrame | None:
    """
    Gets stock data for a specific time period
    :param row: row of sentiment data
    :param eps_df: DataFrame containing EPS data
    :param rev_df: DataFrame containing REV data
    :return: DataFrame containing sentiment and stock data if True else None
    """
    date = row['Date']

    try:
        eps_row = eps_df[eps_df['Date'] < date].sort_values('Date', ascending=False).iloc[0]
        rev_row = rev_df[rev_df['Date'] < date].sort_values('Date', ascending=False).iloc[0]
    except IndexError:
        return None

    row['EPS'] = eps_row['Beat Pred']
    row['REV'] = rev_row['Beat Pred']
    return pd.DataFrame([row])


def prepare_data(
    db_name: str,
    sentiment_table: str,
    earning_table: str,
    earning_dir: str
) -> pd.DataFrame | None:
    """
    Takes data from database's sentiment_table and stock_table and prepares it for analysis
    :param db_name: name of database
    :param sentiment_table: table containing sentiment data
    :param stock_table: table containing stock data
    :param stock_dir: directory containing stock files
    :return: DataFrame containing sentiment and stock data if True else None
    """
    sentiment_df = db_to_df(db_name, sentiment_table)
    earning_df = db_to_df(db_name, earning_table)

    if any(item is None for item in (sentiment_df, earning_df)):
        return None

    sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'])

    valid_symbols = earning_df['Symbol'].unique()
    earning_df.set_index(["Symbol", "Type"], inplace=True)
    grouped_dfs = sentiment_df.groupby(by="Symbol", dropna=True)

    data = []

    for symbol, df in grouped_dfs:
        if symbol not in valid_symbols:
            continue
        
        eps_file = earning_df.loc[(symbol, 'EPS'), 'File']
        rev_file = earning_df.loc[(symbol, 'REV'), 'File']

        eps_df = pd.read_csv(os.path.join(earning_dir, eps_file))
        rev_df = pd.read_csv(os.path.join(earning_dir, rev_file))

        df = df.sort_values(by="Date", ascending=True)

        eps_df['Date'] = pd.to_datetime(eps_df['Date'])
        rev_df['Date'] = pd.to_datetime(rev_df['Date'])

        for i, row in df.iterrows():
            new_row = get_data(row, eps_df, rev_df)

            if new_row is None:
                continue

            data.append(new_row)

    if len(data) == 0:
        return None
    
    new_data = pd.concat(data, ignore_index=True)
    return new_data