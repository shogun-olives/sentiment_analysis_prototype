from src.format_data import format_data
from src.sentiment_analysis import analyze_data
from src.prepare_data import prepare_data
from src.display_data import display_data
import file_helper as fh
import pandas as pd


def main() -> None:
    # TODO download all packages. Run the following in terminal
    # pip install -r requirements.txt

    # TODO modify to work on personal device, paths may be relative or absolute
    # Paths should be with respect to root
    pdf_loc = './raw/transcripts/pdf'
    txt_loc = './raw/transcripts/txt'
    csv_loc = './raw/stock_history/csv'
    format_txt_loc = './files/transcripts'
    format_csv_loc = './files/stock_data'
    db_name = './files/sentiment_analysis_data.db'

    # formats data
    # only execute if converting raw data to formatted
    # TODO Do not mess with this, it could reset the database
    # format_data(pdf_loc, txt_loc, csv_loc, format_txt_loc, format_csv_loc, db_name)

    # sentiment analysis
    # only execute if database does not yet have sentiment analysis
    # TODO Do not mess with this, it could reset the database
    # analyze_data(db_name)

    # prepare data
    # Only execute if data has not yet been prepared for graphing
    # TODO Do not mess with this, it could reset the database
    # prepare(db_name)

    # display data
    # only display data if sentiment analysis has been completed
    # TODO Work in Progress
    # display_data()

    df = fh.db_to_df(db_name, "sentiment_analysis")
    pd.set_option('display.max_rows', None)
    print(df)

    pass


if __name__ == "__main__":
    main()