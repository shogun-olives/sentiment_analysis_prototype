from enum import Enum
from .util import prompt_for_int_input

class Page_Commands(Enum):
    PREVIOUS = 1
    NEXT = 2
    EXIT = 3
    CONTINUE = 4

class Menu:
    """Keeps track of the menu options and their corresponding functions."""

    def __init__(
        self,
        menu_options: dict[str: any] | list[str],
        message: str = None,
        items_per_page: int = 9,
        start_page: int = 1
    ):
        """Keeps track of the menu options and their corresponding functions."""
        if isinstance(menu_options, list):
            menu_options = {option: i+1 for i, option in enumerate(menu_options)}

        self.menu_options: dict[str: any] = menu_options
        self.pages: dict[int:dict[str:any]] = None
        self.message: str = message
        self.items_per_page: int = items_per_page
        self.current_page: int = start_page
        self.create_pages()

    def navigate(self) -> any:
        """
        Prompts the user to select an option and returns the corresponding value
        :return: None
        """
        # Get a string representation of the menu
        menu_text = str(self)

        # If no menu options, return None
        if menu_text is None:
            print("[-] No menu options available")
            return None
        
        # Start on first page of menu and prompt user for input
        self.current_page = 1
        user_input = prompt_for_int_input('[+] ', menu_text, 1, len(self.pages[self.current_page]), True)
        user_input = list(self.pages[self.current_page].keys())[user_input - 1]
        user_selection = self.pages[self.current_page][user_input]

        # If user's selection is not a Page_Command, return the value found at pages[current_page][user_input]
        while isinstance(user_selection, Page_Commands) or isinstance(user_selection, Menu):
            # Logic for navigating pages
            if user_selection == Page_Commands.EXIT:
                break
            elif user_selection == Page_Commands.NEXT:
                self.current_page += 1
            elif user_selection == Page_Commands.PREVIOUS:
                self.current_page -= 1
            
            # If user selects an item that has another menu, return the value from navigating that submenu
            elif isinstance(user_selection, Menu):
                user_selection.set_message(self.message)
                submenu_result = user_selection.navigate()
                if submenu_result == Page_Commands.EXIT:
                    user_selection = Page_Commands.CONTINUE
                    self.current_page = 1
                    continue
                return submenu_result
            
            # After navigating pages, prompt user for input again
            menu_text = str(self)
            user_input = prompt_for_int_input('[+] ', menu_text, 1, len(self.pages[self.current_page]), True)
            user_input = list(self.pages[self.current_page].keys())[user_input - 1]
            user_selection = self.pages[self.current_page][user_input]
        
        # Once they make a non-page selection, return the selection
        return user_selection

    def create_pages(self) -> bool:
        # If no menu options, cannot form pages
        if self.menu_options is None:
            self.pages = None
            return False
        
        # If at most n-1 options, only one page + Exit
        if len(self.menu_options) <= self.items_per_page - 1:
            first_page = self.menu_options
            first_page['Exit'] = Page_Commands.EXIT
            self.pages = {1: first_page}
            return True
        
        # If enough pages to fill more than one page, the first page is the first n-2 options + Next, Exit
        remaining_keys = list(self.menu_options.keys())
        first_page = {key: self.menu_options[key] for key in remaining_keys[:self.items_per_page - 2]}
        first_page['Next'] = Page_Commands.NEXT
        first_page['Exit'] = Page_Commands.EXIT
        pages = {1: first_page}

        # If enough options to fill more than two pages, each page has n-3 options + Previous, Next, Exit
        remaining_keys = remaining_keys[self.items_per_page - 2:]
        while len(remaining_keys) > self.items_per_page - 2:
            temp_page = {key: self.menu_options[key] for key in remaining_keys[:self.items_per_page - 3]}
            remaining_keys = remaining_keys[self.items_per_page - 3:]
            temp_page['Previous'] = Page_Commands.PREVIOUS
            temp_page['Next'] = Page_Commands.NEXT
            temp_page['Exit'] = Page_Commands.EXIT
            pages[len(pages) + 1] = temp_page
        
        # The last page has the remaining options + Previous, Exit
        last_page = {key: self.menu_options[key] for key in remaining_keys}
        last_page['Previous'] = Page_Commands.PREVIOUS
        last_page['Exit'] = Page_Commands.EXIT
        pages[len(pages) + 1] = last_page

        # Set pages to the object's pages
        self.pages = pages
        return True

    def __str__(self) -> str:
        if self.pages is None:
            return None
        
        if self.current_page not in self.pages:
            return NotImplemented
        
        menu_text = ''

        if self.message is not None:
            temp = self.message.split('\n')
            temp = [
                '' if line.strip() == '' else
                f'[!] {line}' if not line.startswith('[!] ') else line
                for line in temp
            ]
            temp = "\n".join(temp)
            menu_text += f'{temp}\n'

        menu_text += "[-] Select an option:"
        for i, option in enumerate(self.pages[self.current_page]):
            menu_text += f"\n{f'[{i+1}]':>7} {option}"

        return menu_text

    def set_page(self, page: int) -> bool:
        """
        Sets the current page of the menu if it is valid.
        :param page: page number
        :return: None
        """
        if page not in self.pages:
            return False
        
        self.current_page = page
        return True
    
    def set_message(self, message: str) -> None:
        """
        Sets the message of the menu
        :param message: message to set
        :return: None
        """
        self.message = message
        self.create_pages()