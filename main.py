import file_helper as fh
import pandas as pd


def format_data() -> None:
    pdf_loc = './raw/transcripts/pdf'
    txt_loc = './raw/transcripts/txt'

    fh.all_pdf_to_txt(pdf_loc, txt_loc, overwrite=False)
    meta_df = fh.get_metadata_df(txt_loc)

    format_txt_loc = './files/transcripts'
    db_name = './files/transcript_metadata.db'

    txt_df = fh.format_all_txt(txt_loc, format_txt_loc)
    df = pd.merge(meta_df, txt_df, on='ID', how='outer')
    fh.df_to_db(df, db_name, 'transcripts')


def get_data() -> pd.DataFrame:
    db_name = './files/transcript_metadata.db'
    df = fh.db_to_df(db_name, 'transcripts')
    return df


def main() -> None:
    # format_data()
    # print(get_data())
    pass


if __name__ == '__main__':
    main()