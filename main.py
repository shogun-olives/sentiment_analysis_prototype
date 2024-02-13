import file_helper as fh
import pandas as pd


def format_data(pdf_loc, txt_loc, format_txt_loc):
    fh.all_pdf_to_txt(pdf_loc, txt_loc, overwrite=False)
    meta_df = fh.get_metadata_df(txt_loc)

    txt_df = fh.format_all_txt(txt_loc, format_txt_loc)

    df = pd.merge(meta_df, txt_df, on='ID', how='outer')
    return df


def main() -> None:
    pdf_loc = './raw/transcripts/pdf'
    txt_loc = './raw/transcripts/txt'
    format_txt_loc = './files/transcripts'
    db_name = './files/sentiment_analysis_data.db'

    # df = format_data(pdf_loc, txt_loc, format_txt_loc)
    # fh.df_to_db(df, db_name, 'transcripts')
    # df = fh.db_to_df(db_name, 'transcripts')
    pass


if __name__ == '__main__':
    main()