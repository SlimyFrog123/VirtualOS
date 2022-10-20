##############################
# IMPORTS
##############################


import os
import sys
import colorama
from vos_priority import Priority


##############################
# FUNCTIONS
##############################


def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

    if os.getenv('INTELLIJ_BASED'):
        return True
    else:
        return supported_platform and is_a_tty


##############################
# LOGGER
##############################


class Logger:
    def __init__(self):
        self.logs: list = list()  # All logs.

        if not supports_color():
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
