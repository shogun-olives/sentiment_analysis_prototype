import os
from ..check_file import dir_exists, not_existing_from_list
from alive_progress import alive_bar


def convert_all(
        conv_func,
        src_ext: str,
        dst_ext: str,
        src_dir: str,
        dst_dir: str = None,
        overwrite: bool = False
) -> bool:
    """
    Converts all files in src_dir to another type in dst_dir
    :param conv_func: function to apply convert all to
    :param src_ext: Original extension (must start with ".")
    :param dst_ext: New extension (must start with ".")
    :param src_dir: Directory with original files
    :param dst_dir: Directory to store new files ([src_dir]_[dst_ext])
    :param overwrite: True to replace all, False to replace none
    :return: True if at least one file succeeded, false otherwise (including not overwritten)
    """
    if dst_dir is None:
        dst_dir = src_dir + f"_{dst_ext}"

    if not dir_exists(src_dir):
        return False

    if not src_ext.startswith('.') or not dst_ext.startswith('.'):
        return False

    dst_files = [
        file.removesuffix(src_ext) + dst_ext
        for file in os.listdir(src_dir)
        if file.endswith(src_ext)
    ]

    if len(dst_files) == 0:
        return False

    if not dir_exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)
    elif not overwrite:
        dst_files = not_existing_from_list(dst_dir, dst_files)
        if len(dst_files) == 0:
            return True

    title = f'{src_ext} to {dst_ext}'
    title = f'{title:<30}'
    success = False
    with alive_bar(len(dst_files), force_tty=True, title=title) as bar:
        for dst_fn in dst_files:
            src_fn = os.path.join(src_dir, dst_fn.removesuffix(dst_ext) + src_ext)
            dst_fn = os.path.join(dst_dir, dst_fn)
            if conv_func(src_fn, dst_fn):
                success = True
            bar()

    return success