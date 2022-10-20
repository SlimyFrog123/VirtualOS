##############################
# IMPORTS
##############################


from vos_logger import Logger
from vos_file_system import FileSystem
from vos_shell_commands import ShellCommands
from vos_shell_lexer import Lexer


##############################
# SHELL
##############################


class Shell:
    def __init__(self, file_system: FileSystem, logger: Logger):
        self.file_system: FileSystem = file_system
        self.logger: Logger = logger
        self.os_info: str = ''

    def __repr__(self):
        return f'Shell({self.file_system}, {self.logger})'

    def initialize(self, os_info):
        self.os_info = os_info

    def run(self):
        shell_commands: ShellCommands = ShellCommands(file_system=self.file_system, os_info=self.os_info)  # Create a shell commands object.

        while True:
            try:
                path_str: str = self.file_system.cwd.as_virtual.path

                if path_str.strip() == '/':
                    path_str = '~'

                input_str: str = input(path_str + '$ ')
                if input_str != '':
                    lexer: Lexer = Lexer(text=input_str, logger=self.logger)  # Create a lexer.
                    tokens = lexer.lex()

                    if len(tokens) > 0:
                        as_admin: bool = False

                        if tokens[0] == 'sudo':
                            as_admin = True
                            tokens.pop(0)

                        output = shell_commands.run(args=tokens, as_admin=as_admin)

                        if not output == '':
                            print(output)
            except KeyboardInterrupt:
                break
