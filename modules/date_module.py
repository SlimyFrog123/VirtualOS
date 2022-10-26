##############################
# IMPORTS
##############################


import datetime


##############################
# MODULE
##############################


def date_command(args: list, as_admin: bool) -> str:
    if '-t' in args:
        return datetime.datetime.now().strftime('%B %d, %Y - %H:%M:%S')
    else:
        return datetime.date.today().strftime('%B %d, %Y')


module: dict = {
    'name': 'date_module',
    'description': 'Module for date-related commands.',
    'version': '1.0',
    'author': 'DJ Cook (@SlimyFrog123)',
    'commands': {
        'date_command': {
            'name': 'date_command',
            'keyword': 'date',
            'description': 'Shows the current date',
            'usage': '\tdate - Shows the current date\n\tdate -t - Shows the current date and time',
            'needs_root': False,
            'needs_fs': False,
            'function': date_command
        }
    }
}
