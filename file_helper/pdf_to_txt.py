"""
This module is used to convert pdf files to txt files
"""
from .shared import file_exists, ensure_fn_path, existing_files
import os
import timeit
from pathlib import Path
from PyPDF2 import PdfReader


def rapid_pdf_to_txt(pdf_path: str, txt_path: str) -> bool:
    """
    Reads in a pdf file and writes it to a text file\n
    Abbreviated version where sanity checks are performed in
    :param pdf_path: path to pdf
    :param txt_path: path to file
    :return: True if process succeeded, otherwise False
    """
    # attempts to read file
    try:
        reader = PdfReader(pdf_path)
    except FileNotFoundError:
        return False
    except EOFError:
        return False

    # write file
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for page in reader.pages:
            txt_file.write(page.extract_text())

    # if no errors, will successfully write txt file
    return True


def pdf_to_txt(pdf_fn: str, txt_fn: str, pdf_directory: str = None, txt_directory: str = None,
               overwrite: bool = None) -> bool:
    """
    Reads in a pdf file and writes it to a text file
    :param pdf_fn: name of pdf file to read
    :param txt_fn: name of file to write
    :param pdf_directory: directory to search for file in, if left blank, defaults to current working directory
    :param txt_directory: directory to search for file in, if left blank, defaults to current working directory
    :param overwrite: True to overwrite all existing files, False to overwrite none, leave None for user prompt
    :return: True if process succeeded, otherwise False
    """
    # exception handling for opening pdf
    if not pdf_fn.endswith('.pdf'):
        return False

    # ensures txt file is properly named
    if not txt_fn.endswith('.txt'):
        txt_fn += '.txt'

    # ensure fn and path are seperated
    pdf_path, pdf_name, pdf_directory = ensure_fn_path(pdf_fn, pdf_directory)
    txt_path, txt_name, txt_directory = ensure_fn_path(txt_fn, txt_directory)

    # attempts to read file
    try:
        reader = PdfReader(pdf_path)
    except FileNotFoundError:
        return False
    except EOFError:
        return False

    # if file exists consider overwrite
    if file_exists(txt_path):
        # if overwrite is None, prompt user
        if overwrite is None:
            print(f"[{txt_fn}] already has data, Overwrite? (y/n)")
            overwrite = input('>>> ')

            # if user chooses not to overwrite, return False
            if not overwrite.lower() == 'y':
                return False

        # if overwrite is False, overwrite skipped
        elif not overwrite:
            return False

    # if directory to file is not cwd and does not exist, create it
    if txt_directory is not None:
        os.makedirs(txt_directory, exist_ok=True)

    # write file
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for page in reader.pages:
            txt_file.write(page.extract_text())

    # if no errors, will successfully write txt file
    return True


def deletion_prompt(files: list[str]) -> list[str]:
    """
    Prompts user to select files to delete
    :param files: list of files marked for deletion
    :return: list of files that are still marked for deletion (can be empty)
    """
    print('The following files already exist')
    for i, file in enumerate(files):
        print(f'\t{i}.\t[{file}]')

    # asks users which files to overwrite
    print("\nOverwrite files? (list indexes of files to keep or 'y' to overwrite all)")
    delete = input(">>> ")
    print()

    # if yes, un-marks all files that already exist
    if delete.lower() in ['y', 'yes', 'confirm']:
        exist = []

    # otherwise, if a list of indexes to keep were supplied, overwrites all except the selected indexes
    elif all(x.isdigit() for x in delete.split(", ")):

        # takes all indexes and removes duplicates then sorts from largest to smallest index
        indexes = list(set(delete.split(", ")))
        indexes.sort(reverse=True)

        # removes all indexes which are out of bounds
        for i in indexes:
            if int(i) > len(files) or int(i) <= 0:
                pass
            else:
                # for remaining valid indexes, removes mark at that index for deletion
                files.pop(int(i) - 1)

    return files


def all_pdf_to_txt(directory: str, destination_directory: str = None, overwrite: bool = None,
                   display_progress: bool = False) -> None:
    """
    Takes all pdf files in directory and converts them to txt files in target_directory
    :param directory: Directory with pdf files
    :param destination_directory: Directory to store txt files in (defaults to [given directory]/../txt)
    :param overwrite: Whether to automatically overwrite all values or not. True to replace all, False to replace none,
    None to prompt user
    :param display_progress: True to show process progress, otherwise writing process gives no print statements
    :return: None
    """
    # if no target directory, sets target directory as txt in the same directory as given directory
    if destination_directory is None:
        destination_directory = os.path.join(os.path.dirname(directory), 'txt')

    # makes sure that given directory is valid
    try:
        os.listdir(directory)
    except FileNotFoundError:
        return None

    # gets list of file names that already exist in target directory and corresponding new name
    pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]
    txt_files = [Path(file).stem + '.txt' for file in pdf_files]

    # if directory exists, find which files already exist in it
    if file_exists(destination_directory):
        exist = existing_files(txt_files, destination_directory)

    # otherwise, create directory and set exists to an empty list
    else:
        os.makedirs(destination_directory, exist_ok=True)
        exist = []

    # If overwrite is None, allow user to choose to overwrite specific files through console
    if overwrite is None:
        exist = deletion_prompt(exist)

    # if overwrite is true, set list of existing files to None
    elif overwrite:
        exist = []

    # if overwrite is false, remove no values from exist
    else:
        pass

    # counters for printing
    count = 0
    t0 = timeit.default_timer()

    if display_progress:
        print('Writing:')

    # creates ultimate list of files to write
    files = [i for i in pdf_files if Path(i).stem + ".txt" not in exist]

    # overwrites all files that are not marked to keep
    for item in files:
        # calculates current and new file name
        pdf_path = os.path.join(directory, item)

        txt_fn = Path(item).stem + ".txt"
        txt_path = os.path.join(destination_directory, txt_fn)

        # writes pdf as txt to new location
        t1 = timeit.default_timer()
        if rapid_pdf_to_txt(pdf_path, txt_path):
            count += 1
            t2 = timeit.default_timer()
            if display_progress:
                print(f"\t{count}.\t[{txt_fn}] written in {t2-t1} sec")

    # prints operation progress
    t3 = timeit.default_timer()
    if display_progress:
        print(f'\nOperation completed in {t3-t0:.2f} seconds')

    # returns nothing
    return None