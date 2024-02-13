import file_helper as fh
import pandas as pd
import timeit


def format_transcript_data(pdf_loc, txt_loc, format_txt_loc):
    # convert all pdf to txt
    fh.all_pdf_to_txt(pdf_loc, txt_loc, overwrite=False)

    # get metadata from txt files
    meta_df = fh.get_metadata_df(txt_loc)

    # format text and get new file names
    txt_df = fh.format_all_txt(txt_loc, format_txt_loc)

    # merge metadata and new file name dataframes
    df = pd.merge(meta_df, txt_df, on='ID', how='outer')
    return df


def main() -> None:
    t1 = timeit.default_timer()
    # defining personal file structure
    pdf_loc = './raw/transcripts/pdf'
    txt_loc = './raw/transcripts/txt'
    format_txt_loc = './files/transcripts'
    db_name = './files/sentiment_analysis_data.db'

    # formatting transcript data
    df = format_transcript_data(pdf_loc, txt_loc, format_txt_loc)
    fh.df_to_db(df, db_name, 'transcripts')

    # reading transcript data
    # df = fh.db_to_df(db_name, 'transcripts')

    t2 = timeit.default_timer()
    print(f'Time elapsed: {t2-t1:.2f} seconds')


if __name__ == '__main__':
    main()