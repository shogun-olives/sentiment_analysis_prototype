from .user_interface import Page_Commands
from .src_config import get_sentiment_analysis_menu


def prompt_user() -> None:
    """
    Prompt user to select an option from the menu. If the user selects an option, execute the function associated with the option.
    :return: None
    """
    # TODO check if user functionality works
    # use menu to get user option
    overwrite_mode = False
    full_menu = get_sentiment_analysis_menu()
    full_menu.set_message(f"Overwrite mode: {"All" if overwrite_mode else "None"}")
    result = full_menu.navigate()
    
    # while result is not exit, continue to prompt user
    while result != Page_Commands.EXIT and result is not None:
        # if result is callable, execute it
        if callable(result):
            try:
                result(overwrite_mode)
            except TypeError:
                result()

        elif result == "Change overwrite state":
            overwrite_mode = not overwrite_mode
            full_menu.set_message(f"Overwrite mode: {"All" if overwrite_mode else "None"}")
        
        result = full_menu.navigate()
    
    # Return None on exit
    return None