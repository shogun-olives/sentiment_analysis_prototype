import file_helper as fh
import os
import pandas as pf
import matplotlib.pyplot as plt


def get_existing_data(db_name: str):
    df = fh.db_to_df(db_name, "sentiment_analysis")
    df.dropna(inplace=True)
    df = df[df["Symbol"] == "NVDA"]
    print(df)

    pass


def display_data():
    pass


def main() -> None:
    db_name = './files/sentiment_analysis_data.db'

    root = '../'
    os.chdir(root)

    get_existing_data(db_name)


if __name__ == "__main__":
    main()