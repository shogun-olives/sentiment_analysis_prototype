import os
from file_helper.db_manager import db_to_df, df_to_db
from file_helper.csv_manager import conditional_delete_row
from alive_progress import alive_bar
import pandas as pd
import numpy as np


def remove_second_row(src_dir: str) -> None:
    src_dir = os.path.abspath(src_dir)
    match_str = 'Average of Absolute Values,,,,,,,,,,,'
    with alive_bar(len(os.listdir(src_dir)), force_tty=True, title='Removing unnecessary data') as bar:
        for file in os.listdir(src_dir):
            if file.endswith('.csv'):
                conditional_delete_row(os.path.join(src_dir, file), match_str)
            bar()


def all_performance_binaries(db_name: str, src_dir: str) -> None:
    src_dir = os.path.abspath(src_dir)
    df = db_to_df(db_name, "transcripts")
    dfs = df.groupby(by="Symbol", dropna=True)
    updated_dfs = []

    files = os.listdir(src_dir)
    with alive_bar(0, force_tty=True, title='Analyzing earnings') as bar:
        for symbol, grouped_df in dfs:
            earnings_files = [file for file in files if symbol.lower() in file.lower()]
            for file in earnings_files:
                performances = performance_binary(grouped_df, os.path.join(src_dir, file))
                if 'EPS' in file:
                    grouped_df = grouped_df.assign(EPS=performances)
                else:
                    grouped_df = grouped_df.assign(REV=performances)
                updated_dfs.append(grouped_df)
                bar()

    df = pd.concat(updated_dfs)
    df = df[['ID', 'Symbol', 'Type', 'neg', 'neu', 'pos', 'EPS', 'REV']]
    df_to_db(df, db_name, 'earnings')


def performance_binary(df: pd.DataFrame, fn: str):
    csv_df = pd.read_csv(fn)
    csv_df = csv_df[['Ann Date', '%Surp']].dropna(inplace=False)
    csv_df['Date'] = pd.to_datetime(csv_df['Ann Date'])
    csv_df['Surplus'] = pd.to_numeric(csv_df['%Surp'].str.removesuffix('%'), errors='coerce').apply(lambda x: 1 if x > 0 else 0)
    csv_df.sort_values('Date', ascending=False, inplace=True)

    performances = []
    for index, row in df.iterrows():
        try:
            performances.append(csv_df[csv_df['Date'] < row['Date']].iloc[0]['Surplus'])
        except IndexError:
            performances.append(np.nan)

    return performances


def main() -> None:
    # Paths should be with respect to root
    db = './files/sentiment_analysis_data.db'
    earnings = r'./files/earnings'
    file = r'C:\Users\Oliver\Documents\Pycharm\sentiment_analysis_prototype\files\earnings\AAPL REV.csv'

    root = '../'
    os.chdir(root)
    all_performance_binaries(db, earnings)


if __name__ == "__main__":
    main()