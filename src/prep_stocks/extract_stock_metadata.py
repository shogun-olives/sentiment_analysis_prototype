"""
This module is used to extract metadata from csv files
"""
from datetime import datetime
import re


def get_metadata(
        fn: str
    ) -> dict[str: str | None]:
    """
    Extracts metadata from file name and contents
    :param fn: name of file to extract metadata from
    :return: dict containing found metadata
    """
    try:
        with open(fn, 'r') as file:
            line = file.readline()
            name_line = line

            for _ in range(3):
                line = file.readline()
            symbol_line = line

            while not line.startswith("History Period:"):
                line = file.readline()
                if not line:
                    break
            date_line = line

            while not line.startswith("VAP: Total"):
                line = file.readline()
                if not line:
                    break
            volume_line = line
            
    except FileNotFoundError or PermissionError:
        return None

    # gets name
    name = name_line.split(" | ")[0]

    # gets symbol
    symbol = symbol_line.split(",")[0].removesuffix(".O")

    # gets dates
    if len(date_line) != 0:
        date_line = date_line.split(",")[0].strip().removeprefix("History Period: ").split(" - ")
        date_format = "%d-%b-%Y"
        start_date = datetime.strptime(data[0], date_format).date()
        end_date = datetime.strptime(data[0], date_format).date()
    else:
        start_date = None
        end_date = None

    # gets volume
    if len(volume_line) != 0:
        volume = "".join(volume_line.split(",")[1:]).strip()
        volume = re.sub(r"[^0-9]", "", volume)
    else:
        volume = None

    data = {
        'Symbol': symbol,
        'Company': name,
        'Start_Date': start_date,
        'End_Date': end_date,
        'Volume': volume,
    }

    return data