"""
Convert txt to pdf
"""
from PyPDF2 import PdfReader
import os
from ..check_file import file_exists
from .convert_all import convert_all


def rapid_pdf_to_txt(
        pdf_path: str,
        txt_path: str
    ) -> bool:
    """
    Abbreviated version where sanity checks are skipped\n
    Reads in a pdf file and writes it to a text file
    :param pdf_path: absolute path to pdf
    :param txt_path: absolute path to file
    :return: True if process succeeded, otherwise False
    """
    try:
        reader = PdfReader(pdf_path)
    except FileNotFoundError or EOFError:
        return False

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for page in reader.pages:
            txt_file.write(page.extract_text())

    return True


def pdf_to_txt(
        pdf_fn: str,
        txt_fn: str,
        overwrite: bool = False
    ) -> bool:
    """
    Reads in a pdf file and writes it to a text file
    :param pdf_fn: name of pdf file to read
    :param txt_fn: name of file to write
    :param overwrite: True to overwrite , False to keep existing
    :return: True if process succeeded, otherwise False
    """
    pdf_fn = os.path.abspath(pdf_fn)
    txt_fn = os.path.abspath(txt_fn)
    
    # exception handling for extensions
    if not pdf_fn.endswith('.pdf') or not txt_fn.endswith('.txt'):
        return False

    # if file exists and overwrite is False, do not overwrite
    if file_exists(txt_fn) and not overwrite:
        return False

    try:
        reader = PdfReader(pdf_fn)
    except FileNotFoundError or EOFError:
        return False

    os.makedirs(os.path.dirname(txt_fn), exist_ok=True)

    with open(txt_fn, "w", encoding="utf-8") as txt_file:
        for page in reader.pages:
            txt_file.write(page.extract_text())

    return True


def all_pdf_to_txt(
        src_dir: str,
        dst_dir: str = None,
        overwrite: bool = False
    ) -> None:
    """
    Converts all pdf files in src_dir to txt files in dst_dir
    :param src_dir: Directory with pdf files
    :param dst_dir: Directory to store txt files ([src_dir]_txt)
    :param overwrite: True to replace all, False to replace none
    :return: None
    """
    convert_all(
        rapid_pdf_to_txt,
        '.pdf', '.txt',
        src_dir, dst_dir,
        overwrite
    )

    return None