import file_helper as fh
import pandas as pd
import os

# TODO rebuild algorithm to work from df to df instead of row by row
def get_data(row: pd.DataFrame, stock_data: pd.DataFrame) -> pd.DataFrame | None:

    start_date = row['Date']
    end_date = start_date + pd.Timedelta(days=7)

    try:
        start_row = stock_data[stock_data['Exchange Date'] < start_date].sort_values('Exchange Date', ascending=False).iloc[0]
        end_row = stock_data[stock_data['Exchange Date'] >= end_date].sort_values('Exchange Date', ascending=True).iloc[0]
    except IndexError:
        return None

    start_perf = start_row['Close']
    end_perf = end_row['Close']

    affect = (end_perf-start_perf)/start_perf

    data = {
        "ID": [row["ID"]],
        "Symbol": [row["Symbol"]],
        "Type": [row["Type"]],
        "neg": [row["neg"]],
        "neu": [row["neu"]],
        "pos": [row["pos"]],
        "Stock": [affect]
    }

    return pd.DataFrame.from_dict(data)

# TODO remember wtf I was doing here
def prepare_data(db_name: str):
    stock_df = fh.db_to_df(db_name, "stock_data")

    sentiment_df = fh.db_to_df(db_name, "transcripts")
    sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'])

    stock_df.set_index("Symbol", inplace=True)

    dfs = sentiment_df.groupby(by="Symbol", dropna=True)

    data = []

    for symbol, df in dfs:
        if symbol not in stock_df.index.values:
            continue

        file = stock_df.loc[symbol, 'File']
        stock_data = pd.read_csv(file)
        df = df.sort_values(by="Date", ascending=True)
        stock_data['Exchange Date'] = pd.to_datetime(stock_data['Exchange Date'])

        for index, row in df.iterrows():
            new_row = get_data(row, stock_data)

            if new_row is None:
                continue

            data.append(new_row)

    new_data = pd.concat(data, ignore_index=True)

    pd.set_option('display.max_columns', None)

    fh.df_to_db(new_data, db_name, "sentiment_analysis")


def main() -> None:
    # Paths should be with respect to root
    db = './files/sentiment_analysis_data.db'

    root = '../'
    os.chdir(root)

    # analyzing entire database
    prepare_data(db)


if __name__ == "__main__":
    main()