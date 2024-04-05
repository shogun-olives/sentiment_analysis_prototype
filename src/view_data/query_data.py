import pandas as pd
from ..file_helper import db_to_df
from ..user_interface import clear_console
from config import file_locations


def display_all_cols() -> None:
    """
    Displays all columns in a dataframe
    :return: None
    """
    pd.set_option('display.max_rows', None)
    pd.options.display.width = 0



def query_stock() -> None:
    """
    Displays stock data until user navigates to next page
    :return: None
    """
    db_name = file_locations['database_db']
    stock_table = file_locations['stock_metadata']
    
    clear_console()
    display_all_cols()

    df = db_to_df(db_name, stock_table)

    print(df)
    print('[-] Press any key to cointinue...')
    input('[+] ')
    return None


def query_sentiment() -> None:
    """
    Displays sentiment analysis until user navigates to next page
    :return: None
    """
    db_name = file_locations['database_db']
    sentiment_table = file_locations['sentiment_analysis_result']

    clear_console()
    display_all_cols()

    df = db_to_df(db_name, sentiment_table)

    print(df)
    print('[-] Press any key to cointinue...')
    input('[+] ')
    return None


def query_earning() -> None:
    """
    Displays earnings until user navigates to next page
    :return: None
    """
    db_name = file_locations['database_db']
    earning_table = file_locations['earning_metadata']

    clear_console()
    display_all_cols()

    df = db_to_df(db_name, earning_table)

    print(df)
    print('[-] Press any key to cointinue...')
    input('[+] ')
    return None


def query_transcript() -> None:
    """
    Displays transcripts until user navigates to next page
    :return: None
    """
    db_name = file_locations['database_db']
    transcript_table = file_locations['transcript_metadata']

    clear_console()
    display_all_cols()

    df = db_to_df(db_name, transcript_table)

    print(df)
    print('[-] Press any key to cointinue...')
    input('[+] ')
    return None

# TODO Add functionality to these functions
# TODO allow for filtering
# TODO allow for sorting
# TODO Figure out submenu for filtering and sorting