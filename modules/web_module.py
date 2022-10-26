##############################
# IMPORTS
##############################


import os
import requests
import urllib.request
from vos_file_system import FileSystem, Path


##############################
# MODULE
##############################


def wprint_command(args: list, as_admin: bool) -> str:
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


def download(url: str, file: Path):
    try:
        urllib.request.urlretrieve(url, file.as_local.path)
        return f'File successfully saved as {file.as_virtual.path}.'
    except Exception as e:
        return f'Error: {e}.'


def wget_command(args: list, as_admin: bool, file_system: FileSystem) -> str:
    if len(args) == 0:
        return 'Please specify a url to download from.'
    elif len(args) == 1:
        return 'Please specify a file to download to.'
    else:
        url = args[0]
        file = Path(args[1])

        if os.path.exists(file.as_local.path):
            if input('File already exists. Overwrite? [Y/n] ') == 'Y':
                return download(url=url, file=file)
            else:
                return 'Download cancelled.'
        else:
            return download(url=url, file=file)


module: dict = {
    'name': 'web_module',
    'description': 'Module for web-related commands.',
    'version': '1.0',
    'author': 'DJ Cook (@SlimyFrog123)',
    'commands': {
        'wprint_command': {
            'name': 'wprint',
            'keyword': 'wprint',
            'description': 'Prints the contents of a website.',
            'usage': '\twprint <url> - Prints the contents of a website.',
            'needs_root': False,
            'needs_fs': False,
            'function': wprint_command
        },
        'wget_command': {
            'name': 'wget',
            'keyword': 'wget',
            'description': 'Downloads a file from a website.',
            'usage': '\twget <url> <file> - Downloads a file from a website.',
            'needs_root': False,
            'needs_fs': True,
            'function': wget_command
        }
    }
}
