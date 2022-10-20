##############################
# IMPORTS
##############################


import os
import subprocess
import pathlib

from vos_logger import Logger


##############################
# CONSTANTS
##############################


FILE_SYSTEM_START = pathlib.Path(__file__).resolve().parent
FILE_SYSTEM_ROOT = pathlib.Path.joinpath(FILE_SYSTEM_START, 'vos_fs')  # The root of the file system.


##############################
# PATH
##############################


class Path:
    def __init__(self, filepath: str):
        self.path: str = filepath

    def __repr__(self):
        return f'Path({self.path})'

    @property
    def as_virtual(self):
        path = self.path

        path = path.replace(str(FILE_SYSTEM_ROOT), '')
        path = path.replace('\\', '/')

        if not path.startswith('/'):
            path = '/' + path

        return Path(path)

    @property
    def as_local(self):
        path = self.path

        path = path.replace('/', '\\')
        if not path.startswith(str(FILE_SYSTEM_ROOT)):
            if not path.startswith('\\'):
                path = '\\' + path

            fs_rs = str(FILE_SYSTEM_ROOT).rstrip('\\')
            path = f'{fs_rs}{path}'

        return Path(path)


##############################
# FILE SYSTEM
##############################


class FileSystem:
    def __init__(self, logger: Logger, root: str = None):
        # Root directory of the file system.
        if root is None:
            self.root: Path = Path(str(FILE_SYSTEM_ROOT))
        else:
            self.root: Path = Path(root)

        self.logger = logger

        self.cwd: Path = self.root  # Current Working Directory.
        self.cwd_dirs: list = list()  # Current Working Directory's Directories.
        self.cwd_files: list = list()  # Current Working Directory's Files.

    def __repr__(self):
        return f'FileSystem(root={self.root}, cwd={self.cwd})'

    def initialize(self):
        if not os.path.exists(self.root.path):
            os.mkdir(self.root.path)

    def list_cwd(self) -> str:
        return_str: str = ''

        self.cwd_dirs = list()
        self.cwd_files = list()

        for item in os.listdir(self.cwd.path):
            if os.path.isdir(os.path.join(self.cwd.path, item)):
                self.cwd_dirs.append(item)
                return_str += f'{item}/\n'
            else:
                self.cwd_files.append(item)
                return_str += f'{item}\n'

        return_str = return_str.rstrip('\n')  # Remove the trailing newline.

        return return_str

    def change_dir(self, path: Path) -> str:
        if path.path.isspace() or path.path == '/' or path.path == '~':
            self.cwd = self.root
            return ''

        if path.path == '..':
            if not self.cwd == self.root:
                target_path = Path(str(pathlib.Path(self.cwd.path).parent))

                if os.path.exists(target_path.path):
                    self.cwd = target_path
                    return ''
            else:
                return ''

        if path.path.startswith('/'):
            # Absolute path from the start of the file system.
            attempted_path: Path = path.as_virtual

            if os.path.exists(attempted_path.path) and os.path.isdir(attempted_path.path):
                self.cwd = attempted_path
                return ''
            else:
                return f'No such directory: {attempted_path.path}'
        else:
            # Relative path from the current working directory.
            attempted_path: Path = Path(os.path.join(self.cwd.path, path.as_local.path))

            if os.path.exists(attempted_path.path) and os.path.isdir(attempted_path.path):
                self.cwd = attempted_path
                return ''
            else:
                return f'No such directory: {attempted_path.path}'

    def run_python_script(self, filepath: str) -> str:
        path: Path = Path(str(filepath))

        if path.path.startswith('/'):
            script_path: Path = path.as_local
        else:
            script_path: Path = Path(self.cwd.path + '\\' + path.path)

        if os.path.exists(script_path.path):
            process = subprocess.run(['python', script_path.path], cwd=self.cwd.as_local.path)
            return str(process.stdout)
        else:
            return f'No such file: {script_path.path}'
