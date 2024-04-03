from ..file_helper import db_to_df
import pandas as pd
import os

def get_data(
    row: pd.Series,
    stock_data: pd.DataFrame,
    time_period: int = 3
) -> pd.DataFrame | None:
    """
    Gets stock data for a specific time period
    :param row: row of sentiment data
    :param stock_data: DataFrame containing stock data
    :param time_period: number of days to look at stock data
    :return: DataFrame containing sentiment and stock data if True else None
    """
    start_date = row['Date']
    end_date = start_date + pd.Timedelta(days=time_period)

    try:
        start_row = stock_data[stock_data['Exchange Date'] < start_date].sort_values('Exchange Date', ascending=False).iloc[0]
        end_row = stock_data[stock_data['Exchange Date'] >= end_date].sort_values('Exchange Date', ascending=True).iloc[0]
    except IndexError:
        return None

    start_perf = start_row['Close']
    end_perf = end_row['Close']

    affect = (end_perf-start_perf)/start_perf

    row['Stock'] = affect
    return pd.DataFrame([row])


def prepare_data(
    db_name: str,
    sentiment_table: str,
    stock_table: str,
    stock_dir: str,
    time_period: int = 3
) -> pd.DataFrame | None:
    """
    Takes data from database's sentiment_table and stock_table and prepares it for analysis
    :param db_name: name of database
    :param sentiment_table: table containing sentiment data
    :param stock_table: table containing stock data
    :param stock_dir: directory containing stock files
    :param time_period: number of days to look at stock data
    :return: DataFrame containing sentiment and stock data if True else None
    """
    sentiment_df = db_to_df(db_name, sentiment_table)
    stock_df = db_to_df(db_name, stock_table)

    if any(item is None for item in (sentiment_df, stock_df)):
        return None

    sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'])

    stock_df.set_index("Symbol", inplace=True)
    grouped_dfs = sentiment_df.groupby(by="Symbol", dropna=True)

    data = []

    for symbol, df in grouped_dfs:
        if symbol not in stock_df.index.values:
            continue

        file = stock_df.loc[symbol, 'File']
        stock_data = pd.read_csv(os.path.join(stock_dir, file))
        df = df.sort_values(by="Date", ascending=True)
        stock_data['Exchange Date'] = pd.to_datetime(stock_data['Exchange Date'])

        for i, row in df.iterrows():
            new_row = get_data(row, stock_data, time_period)

            if new_row is None:
                continue

            data.append(new_row)

    new_data = pd.concat(data, ignore_index=True)
    return new_data