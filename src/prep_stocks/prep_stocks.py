from .format_stock_data import format_all_stocks
from ..file_helper import df_to_db
from config import file_locations


def prep_stocks(
    overwrite: bool = False
) -> bool:
    """
    Takes config data to format stocks
    :param overwrite: If True, overwrite existing files
    :return: True if successful, False otherwise
    """
    csv_src_dir = file_locations['original_stock_csv']
    csv_dst_dir = file_locations['formatted_stock_csv']
    db_name = file_locations['database_db']
    table_name = file_locations['stock_metadata']

    # format transcripts
    result = format_all_stocks(csv_src_dir, csv_dst_dir, overwrite)
    if result is None:
        return False

    # Update Database
    if not df_to_db(result, db_name, table_name):
        return False

    return True