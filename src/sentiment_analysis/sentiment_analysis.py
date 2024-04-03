from ..file_helper import db_to_df, df_to_db
from .preprocess import preprocess_all
from .nltk_sentiment_analysis import nltk_analyze_all
import pandas as pd
from config import file_locations


def sentiment_analysis(
    overwrite: bool = False
) -> bool:
    """
    Takes config data to preprocess formatted transcripts and do NLTK vader sentiment analysis
    :param overwrite: If True, overwrite existing files
    :return: True if successful, False otherwise
    """
    src_dir = file_locations['formatted_transcripts_txt']
    dst_dir = file_locations['processed_transcripts_txt']
    db_name = file_locations['database_db']
    transcript_table_name = file_locations['transcript_metadata']
    sentiment_table_name = file_locations['sentiment_analysis_result']

    if not preprocess_all(src_dir, dst_dir, overwrite):
        return False
    
    transcript_df = db_to_df(db_name, transcript_table_name)
    if transcript_df is None:
        return False

    sentiment_df = db_to_df(db_name, sentiment_table_name)
    if sentiment_df is None or overwrite:
        sentiment_df = nltk_analyze_all(dst_dir)
    else:
        return True
    
    df = pd.merge(transcript_df, sentiment_df, on='File', how='outer')
    if not df_to_db(df, db_name, sentiment_table_name):
        return False
    
    return True


def sentiment_analysis_preprocess(
    overwrite: bool = False
) -> bool:
    """
    Preprocesses all formatted transcripts
    :param overwrite: If True, overwrite existing files
    :return: True if successful, False otherwise
    """
    src_dir = file_locations['formatted_transcripts_txt']
    dst_dir = file_locations['processed_transcripts_txt']

    return preprocess_all(src_dir, dst_dir, overwrite)


def sentiment_analysis_nltk(
    overwrite: bool = False
) -> bool:
    """
    Does NLTK vader sentiment analysis on all processed transcripts
    :param overwrite: If True, overwrite existing files
    :return: True if successful, False otherwise
    """
    dst_dir = file_locations['processed_transcripts_txt']
    db_name = file_locations['database_db']
    transcript_table_name = file_locations['transcript_metadata']
    sentiment_table_name = file_locations['sentiment_analysis_result']

    transcript_df = db_to_df(db_name, transcript_table_name)
    if transcript_df is None:
        return False

    sentiment_df = db_to_df(db_name, sentiment_table_name)
    if sentiment_df is None or overwrite:
        sentiment_df = nltk_analyze_all(dst_dir)
    else:
        return True
    
    sentiment_df = nltk_analyze_all(dst_dir)
    if sentiment_df is None:
        return False

    df = pd.merge(transcript_df, sentiment_df, on='File', how='outer')
    if not df_to_db(df, db_name, sentiment_table_name):
        return False
    
    return True