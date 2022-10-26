##############################
# IMPORTS
##############################


import requests
from vos_file_system import FileSystem


##############################
# MODULE
##############################


def wprint_command(args: list, as_admin: bool, file_system: FileSystem) -> str:
    if len(args) == 0:
        return 'Please specify a url to print from.'
    else:
        try:
            return requests.get(args[0]).text
        except requests.exceptions.MissingSchema:
            return 'Invalid url.'
        except requests.exceptions.ConnectionError:
            return 'Connection error.'
        except requests.exceptions.InvalidURL:
            return 'Invalid url.'
        except requests.exceptions.InvalidSchema:
            return 'Invalid url.'
        except requests.exceptions.TooManyRedirects:
            return 'Too many redirects.'


module: dict = {
    'name': 'web_module',
    'description': 'Module for web-related commands.',
    'version': '1.0',
    'author': 'DJ Cook (@SlimyFrog123)',
    'commands': {
        'wprint_command': {
            'name': 'wprint_command',
            'keyword': 'wprint',
            'description': 'Prints the contents of a website.',
            'usage': '\twprint <url> - Prints the contents of a website.',
            'needs_root': False,
            'needs_fs': True,
            'function': wprint_command
        }
    }
}
