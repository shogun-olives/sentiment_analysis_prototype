import os


def clear_console() -> None:
    print()
    os.system('cls' if os.name == 'nt' else 'clear')


def is_int(
        s: str
) -> bool:
    """
    Checks if string is an integer
    :param s: string to check
    :return: True if string is an integer, otherwise False
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def prompt_for_int_input(
    prompt: str,
    pre_text: str = None,
    min_val: int = None,
    max_val: int = None,
    clear: bool = False
) -> int:
    """
    Prompts user for an integer input
    :param prompt: prompt to display to user
    :param pre_text: text to display before error message and prompt
    :param min_val: minimum value for input
    :param max_val: maximum value for input
    :param clear: clear console before prompting user
    :return: integer input
    """
    error = None
    while True:
        if clear:
            clear_console()
        
        if pre_text is not None:
            print(pre_text)
        
        if error is not None:
            print(f"[!] {error}")
        
        user_input = input(prompt)

        if not is_int(user_input):
            error = "Input must be an integer"
            continue

        user_input = int(user_input)
        
        if min_val is not None and user_input < min_val:
            error = f"Input min: {min_val}"
            continue

        if max_val is not None and user_input > max_val:
            error = f"Input max: {max_val}"
            continue
        
        return user_input