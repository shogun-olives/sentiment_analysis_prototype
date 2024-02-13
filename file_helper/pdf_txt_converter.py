import os
import timeit
from pathlib import Path
from PyPDF2 import PdfReader


def file_exists(fn) -> bool:
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
    if not pdf_fn.endswith('.pdf'):
        return False

    try:
        reader = PdfReader(pdf_fn)
    except FileNotFoundError:
        print(f"[{pdf_fn}] not found")
        return False
    except EOFError:
        print(f"[{pdf_fn}] has an invalid end of file")
        return False

    # if file exists and overwrite is false prompt user to overwrite
    if not overwrite_all and file_exists(txt_fn):
        print(f"[{txt_fn}] already has data, Overwrite? (y/n)")
        overwrite = input('>>> ')
        if not overwrite.lower() == 'y':
            return False

    # if directory to file does not exist, create it
    os.makedirs(os.path.dirname(txt_fn), exist_ok=True)

    # write file
    with open(txt_fn, "w", encoding="utf-8") as txt_file:
        try:
            for page in reader.pages:
                txt_file.write(page.extract_text())
        except OSError as error:
            print(error)
            return False

    return True


def all_pdf_to_txt(dir_name: str, target_dir: str = None, overwrite: bool = None) -> None:
    # if no target directory, create target directory as txt in the same directory
    if target_dir is None:
        target_dir = os.path.join(os.path.dirname(dir_name), 'txt')

    # check for files that already exist
    if overwrite is None:
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
    elif overwrite:
        exist = []
    else:
        exist = []
        for item in os.listdir(dir_name):
            txt_fn = item.removesuffix('.pdf') + ".txt"
            if file_exists(os.path.join(target_dir, txt_fn)):
                exist.append(item)

    # overwrites all files that are not marked to keep
    count = 0
    delim = '\t\t'
    t0 = timeit.default_timer()
    files = [i for i in os.listdir(dir_name) if i not in exist]
    for item in files:

        # calculates current and destination
        txt_fn = Path(item).stem + ".txt"
        curr = os.path.join(dir_name, item)
        dest = os.path.join(target_dir, txt_fn)

        # writes pdf to new location
        t1 = timeit.default_timer()
        if pdf_to_txt(curr, dest, overwrite_all=True):
            count += 1
            if count >= 100:
                delim = '\t'
            t2 = timeit.default_timer()
            print(f"{count}.{delim}[{txt_fn}] written in {t2-t1} sec")

        t3 = timeit.default_timer()
        if overwrite is not False:
            print(f'\nOperation completed in {t3-t0:.2f} seconds')

        return None