import file_helper as fh
import pandas as pd
import timeit
import os


def format_transcript_data(pdf_loc, txt_loc, format_txt_loc):
    """
    Convenience function to format all transcript data
    :param pdf_loc: directory of pdfs
    :param txt_loc: directory to store txt files
    :param format_txt_loc: directory to store formatted txt files
    :return: dataframe with metadata and file locations
    """
    fh.all_pdf_to_txt(pdf_loc, txt_loc, overwrite=False, display_progress=False)
    meta_df = fh.txt_get_all_metadata(txt_loc)
    txt_df = fh.format_all_txt(txt_loc, format_txt_loc, overwrite=False)
    df = pd.merge(meta_df, txt_df, on='ID', how='outer')
    return df


def format_stock_data(csv_loc, format_csv_loc):
    """
    Convenience function to format all stock data
    :param csv_loc: directory of csvs
    :param format_csv_loc: directory to store formatted csv files
    :return: dataframe with metadata and file locations
    """
    meta_df = fh.csv_get_all_metadata(csv_loc)
    csv_df = fh.format_all_csv(csv_loc, format_csv_loc, overwrite=False)
    df = pd.merge(meta_df, csv_df, on='Company', how='outer')
    return df


def format_data(pdf_loc: str, txt_loc: str, csv_loc: str, format_txt_loc: str, format_csv_loc: str, db_name: str
                ) -> None:
    """
    Convenience function to format all data from pdf and raw csv to formatted txt and csv files
    :param pdf_loc: original location of pdfs
    :param txt_loc: location to store txt
    :param csv_loc: original location of csvs
    :param format_txt_loc: location to store formatted txt
    :param format_csv_loc: location to store formatted csv
    :param db_name: location of dataframe
    :return: None
    """
    print('Data formatting in progress...')
    # start timing process
    t1 = timeit.default_timer()

    # formatting transcript data
    txt_df = format_transcript_data(pdf_loc, txt_loc, format_txt_loc)
    fh.df_to_db(txt_df, db_name, 'transcripts')

    # formatting csv data
    csv_df = format_stock_data(csv_loc, format_csv_loc)
    fh.df_to_db(csv_df, db_name, 'stock_data')

    # end timing process
    t2 = timeit.default_timer()
    print(f'Time elapsed: {t2 - t1:.2f} seconds')


def main() -> None:
    # TODO modify to work on personal device, paths may be relative or absolute
    # Paths should be with respect to root
    pdf_loc = './raw/transcripts/pdf'
    txt_loc = './raw/transcripts/txt'
    csv_loc = './raw/stock_history/csv'
    format_txt_loc = './files/transcripts'
    format_csv_loc = './files/stock_data'
    db_name = './files/sentiment_analysis_data.db'

    root = '../'
    os.chdir(root)

    format_data(pdf_loc, txt_loc, csv_loc, format_txt_loc, format_csv_loc, db_name)


if __name__ == '__main__':
    main()