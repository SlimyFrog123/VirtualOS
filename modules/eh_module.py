##############################
# IMPORTS
##############################


import art
import socket
import urllib.parse
from tqdm import tqdm
from datetime import datetime


##############################
# MODULE
##############################


def port_scan_command(args: list, as_admin: bool) -> str:
    if len(args) == 0:
        return 'No target specified.'
    else:
        uri = urllib.parse.urlparse(args[0])

        hostname = uri.netloc or str(args[0])

        target = socket.gethostbyname(hostname)

        print(art.text2art('PORTSCAN'))

        print('-' * 50)
        print('Scanning target ' + target + (f':{args[1]}' if len(args) > 1 else '') + f' ({hostname})')
        print('Time started: ' + str(datetime.now().strftime("%H:%M:%S")))
        print('-' * 50)
        if len(args) == 1:
            print('\nThis may take a while, scanning 65535 ports...')

        try:
            if len(args) == 1:
                for port in tqdm(range(1, 65535), desc='Scanning Ports', ascii=False, unit='Port'):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(1)
                    result = s.connect_ex((target, port))

                    if result == 0:
                        print(f'\nPort {port} is open.')
                    s.close()
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = s.connect_ex((target, int(args[1])))

                s.close()

                if result == 0:
                    return f'Port {int(args[1])} is open.'
                else:
                    return f'Port {int(args[1])} is closed.'
        except KeyboardInterrupt:
            return '\nOperation Cancelled.'
        except socket.gaierror:
            return '\nHostname could not be resolved.'
        except socket.error:
            return 'Couldn\'t connect to server.'
        except Exception as e:
            return f'Error: {e}.'


module: dict = {
    'name': 'Ethical Hacking Module',
    'description': 'Module for ethical hacking-related commands.',
    'version': '1.0.0',
    'author': 'DJ Cook (@SlimyFrog123)',
    'commands': {
        'port_scan': {
            'name': 'portscan',
            'keyword': 'portscan',
            'description': 'Scans a target for open ports.',
            'usage': '\tportscan <target> - Scans a target for open ports.\n\tportscan <target> <port> - Scans a target'
                     ' for a specific port.',
            'needs_root': False,
            'needs_fs': False,
            'function': port_scan_command
        }
    }
}
