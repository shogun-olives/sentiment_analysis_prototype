from .format_earnings import format_all_earnings
from ..file_helper import df_to_db, all_xlsx_to_csv
from config import file_locations


def prep_earnings(
    overwrite: bool = False
) -> bool:
    """
    Takes config data to format earnings
    :param overwrite: overwrite existing data
    :return: True if successful, False otherwise
    """
    xlsx_dir = file_locations['original_earnings_xlsx']
    csv_src_dir = file_locations['original_earnings_csv']
    csv_dst_dir = file_locations['formatted_earnings_csv']
    db_name = file_locations['database_db']
    table_name = file_locations['earning_data']

    # convert xlsx to csv
    if not all_xlsx_to_csv(xlsx_dir, csv_src_dir, overwrite):
        return False
    
    # format earnings
    result = format_all_earnings(csv_src_dir, csv_dst_dir, overwrite)
    if result is None:
        return False

    # Update Database
    if not df_to_db(result, db_name, table_name):
        return False

    return True



def earning_xlsx_to_csv(
    overwrite: bool = False
) -> bool:
    """
    Converts all xlsx files in xlsx_dir to csv files in csv_dir
    :param xlsx_dir: directory of xlsx files
    :param csv_dir: directory of csv files
    :param overwrite: overwrite existing data
    :return: True if successful, False otherwise
    """
    xlsx_dir = file_locations['original_earnings_xlsx']
    csv_dir = file_locations['original_earnings_csv']

    return all_xlsx_to_csv(xlsx_dir, csv_dir, overwrite)


def earning_format(
    overwrite: bool = False
) -> bool:
    """
    Formats all csv files in src_dir and saves them to dst_dir
    :param src_dir: directory of csv files
    :param dst_dir: directory to save formatted csv files
    :param overwrite: overwrite existing data
    :return: True if successful, False otherwise
    """
    src_dir = file_locations['original_earnings_csv']
    dst_dir = file_locations['formatted_earnings_csv']
    db_name = file_locations['database_db']
    table_name = file_locations['earning_data']

    result = format_all_earnings(src_dir, dst_dir, overwrite)
    if result is None:
        return False

    # Update Database
    if not df_to_db(result, db_name, table_name):
        return False

    return True