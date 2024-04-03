from ..file_helper import all_pdf_to_txt, df_to_db
from .format_transcripts import format_all_transcripts
from config import file_locations


def prep_transcripts(
    overwrite: bool = False
) -> bool:
    """
    Takes config data to convert pdf transcripts to formatted transcripts
    :param overwrite: If True, overwrite existing files
    :return: True if successful, False otherwise
    """
    pdf_dir = file_locations['original_transcripts_pdf']
    txt_src_dir = file_locations['original_transcripts_txt']
    txt_dst_dir = file_locations['formatted_transcripts_txt']
    db_name = file_locations['database_db']
    table_name = file_locations['transcript_metadata']
    
    # convert pdf to txt
    if not all_pdf_to_txt(pdf_dir, txt_src_dir, overwrite):
        return False

    # format transcripts
    result = format_all_transcripts(txt_src_dir, txt_dst_dir, overwrite)
    if result is None:
        return False

    # Update Database
    if not df_to_db(result, db_name, table_name):
        return False

    return True


def transcript_pdf_to_txt(
    overwrite: bool = True
) -> bool:
    """
    Converts all pdf transcripts to txt
    :param overwrite: If True, overwrite existing files
    :return: True if successful, False otherwise
    """
    pdf_dir = file_locations['original_transcripts_pdf']
    txt_src_dir = file_locations['original_transcripts_txt']

    return all_pdf_to_txt(pdf_dir, txt_src_dir, overwrite)


def transcripts_format(
    overwrite: bool = True
) -> bool:
    """
    Formats all transcripts
    :param overwrite: If True, overwrite existing files
    :return: True if successful, False otherwise
    """
    txt_src_dir = file_locations['original_transcripts_txt']
    txt_dst_dir = file_locations['formatted_transcripts_txt']
    db_name = file_locations['database_db']
    table_name = file_locations['transcript_metadata']

    transcript_df = format_all_transcripts(txt_src_dir, txt_dst_dir, overwrite)
    if transcript_df is None:
        return False
    
    if not df_to_db(transcript_df, db_name, table_name):
        return False
    
    return True