##############################
# IMPORTS
##############################


import colorama
from vos_priority import Priority


##############################
# LOGGER
##############################


class Logger:
    def __init__(self, is_internal: bool = True):
        self.logs: list = list()  # All logs.

        if not is_internal:
            colorama.init(convert=True)  # Initialize colorama.

    def log(self, message: str, priority: Priority = Priority.NONE):
        if priority == Priority.NONE:
            print(message)
        elif priority == Priority.LOW:
            print(colorama.Fore.GREEN + colorama.Style.DIM + message + colorama.Style.RESET_ALL)
        elif priority == Priority.MEDIUM:
            print(colorama.Fore.YELLOW + message + colorama.Style.RESET_ALL)
        elif priority == Priority.HIGH:
            print(colorama.Fore.RED + message + colorama.Style.RESET_ALL)
        elif priority == Priority.CRITICAL:
            print('\033[4m' + colorama.Fore.RED + colorama.Style.BRIGHT + message + colorama.Style.RESET_ALL)

        log_ = {
            'message': message,
            'priority': priority
        }

        self.logs.append(log_)  # Save the log for future access.

    def __repr__(self):
        return f'Logger()'
