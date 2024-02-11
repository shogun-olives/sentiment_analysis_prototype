import os
from pdfminer.high_level import extract_text
from pathlib import Path
from PyPDF2 import PdfReader
from pdfminer.pdfparser import PDFSyntaxError
import time


def file_exists(fn):
    # checks if file exists
    if not os.path.exists(fn):
        return False

    # checks if file has data
    if os.path.getsize(fn) == 0:
        return False

    # if file doesn't exist or has no data, return true
    return True


def pdf_to_txt(pdf_fn: str, txt_fn: str, overwrite_all: bool = False) -> bool:
    # exception handling for opening pdf
    t1 = time.clock()
    try:
        reader = PdfReader("example.pdf")
    except FileNotFoundError:
        print(f"[{pdf_fn}] not found")
        return False
    except PDFSyntaxError:
        print(f"[{pdf_fn}] has an invalid format")
        return False
    t2 = time.clock()
    print(f"[Reading pdf] {t2-t1} seconds")

    t1 = time.clock()
    # if file exists and overwrite is false prompt user to overwrite
    if not overwrite_all and file_exists(txt_fn):
        print(f"[{txt_fn}] already has data, Overwrite? (y/n)")
        overwrite = input('>>> ')
        if not overwrite.lower() == 'y':
            return False
    t2 = time.clock()
    print(f"[Checking overwrite] {t2 - t1} seconds")

    t1 = time.clock()
    # if directory to file does not exist, create it
    os.makedirs(os.path.dirname(txt_fn), exist_ok=True)
    t2 = time.clock()
    print(f"[Directory check] {t2 - t1} seconds")

    t1 = time.clock()
    # write file
    with open(txt_fn, "w", encoding="utf-8") as txt_file:
        try:
            for page in reader.pages:
                txt_file.write(page.extract_text())
        except OSError as error:
            print(error)
            return False
    t2 = time.clock()
    print(f"[Write File] {t2 - t1} seconds")

    return True


def all_pdf_to_txt(dir_name: str, target_dir: str = None) -> None:
    # if no target directory, create target directory as txt in the same directory
    if target_dir is None:
        target_dir = os.path.join(os.path.dirname(dir_name), 'txt')

    # check for files that already exist
    exist = []
    for item in os.listdir(dir_name):
        txt_fn = item.removesuffix('.pdf') + ".txt"
        if file_exists(os.path.join(target_dir, txt_fn)):
            exist.append(item)
            print(f'{str(len(exist))}.\t{item}')

    # asks users which files to overwrite
    print("\nOverwrite files? (list indexes of files to keep or 'y' to overwrite all)")
    delete = input(">>> ")
    print()

    # if yes, unmarks all files that already exist
    if delete.lower() in ['y', 'yes', 'confirm']:
        exist = []

    # otherwise, if a list of indexes to keep were supplied, overwrites all except the selected indexes
    elif all(x.isdigit() for x in delete.split(", ")):

        # takes all indexes and removes duplicates then sorts from largest to smallest index
        indexes = list(set(delete.split(", ")))
        indexes.sort(reverse=True)

        # removes all indexes which are out of bounds
        for i in indexes:
            if int(i) > len(exist) or int(i) <= 0:
                print(f'{i} is not a valid index')
            else:
                # for remaining valid indexes, removes mark at that index for deletion
                exist.pop(int(i) - 1)

    # overwrites all files that are not marked to keep
    count = 0
    delim = '\t\t'
    for item in os.listdir(dir_name):
        if item in exist:
            continue
        txt_fn = Path(item).stem + ".txt"
        if pdf_to_txt(os.path.join(dir_name, item), os.path.join(target_dir, txt_fn), overwrite_all=True):
            count += 1
            if count >= 100:
                delim = '\t'
            print(f"{count}.{delim}[{txt_fn}] written")

    pass