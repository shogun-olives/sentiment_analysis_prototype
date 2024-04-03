"""
Module containing functions shared across src
"""


def find_index(
        array: list[str],
        substr: str | list[str]
) -> int | None:
    """
    Finds first string in array containing substr
    :param array: list of strings
    :param substr: substring to search for or list of substrings to search for
    :return: index if found, otherwise None
    """
    if isinstance(substr, str):
        substr = [substr]

    for i, item in enumerate(array):
        if any(sub in item for sub in substr):
            return i
    
    return None


def merge_dicts(
        dict_1: dict,
        dict_2: dict
) -> dict[any:list[any]]:
    """
    Merges two dicts\n
    For each key:\n
    \tIf key is in both dicts, value is list containing both values\n
    \tIf key is only in one key, value is list with one item\n
    \tIf value in both dicts is a list, value is a 2d array\n
    \tIf value in only one dict is a list, value is list extended by other value\n
    :param dict_1: first dict
    :param dict_2: second dict
    :return: Merged dict
    """
    keys = list(dict_1.keys())
    keys += [key for key in dict_2.keys() if key not in keys]
    final_dict = dict()

    for key in keys:
        if key in dict_1 and key in dict_2:

            if isinstance(dict_1[key], list) and isinstance(dict_2[key], list):
                final_dict[key] = dict_1[key] + dict_2[key]
            elif isinstance(dict_1[key], list):
                final_dict[key] = dict_1[key] + [dict_2[key]]
            elif isinstance(dict_2[key], list):
                final_dict[key] = [dict_1[key]] + dict_2[key]
            else:
                final_dict[key] = [dict_1[key], dict_2[key]]
        elif key in dict_1:
            final_dict[key] = [dict_1[key]]
        elif key in dict_2:
            final_dict[key] = [dict_2[key]]
    
    return final_dict