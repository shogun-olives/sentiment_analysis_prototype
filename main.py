import file_helper as fh


def main() -> None:
    df = fh.get_metadata_df('./raw/transcripts/txt')
    fh.df_to_db(df, './files/transcript_metadata.db', 'transcripts')


if __name__ == '__main__':
    main()