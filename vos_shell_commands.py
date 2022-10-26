##############################
# IMPORTS
##############################


import os
from vos_commands import Command, CommandInfo
from vos_file_system import FileSystem, Path
from vos_module_loader import ModuleLoader
from vos_logger import Logger
from vos_priority import Priority
from vos_shell_lexer import Lexer


##############################
# SHELL COMMANDS
##############################


class ShellCommands:
    def __init__(self, file_system: FileSystem, os_info: str, logger: Logger):
        self.commands: dict = {}
        self.file_system: FileSystem = file_system
        self.os_info = os_info
        self.logger = logger
        self.module_loader: ModuleLoader = ModuleLoader(logger=self.logger)
        self.initialize()

    def initialize(self):
        """Initializes the shell commands."""
        _help_command_info: CommandInfo = CommandInfo(name='help', description='Displays help for a command.',
                                                      usage='\thelp <command> - Displays help for a specific '
                                                            'command.\n\thelp -a - Displays help for all commands.')
        _help_command: Command = Command('help', _help_command_info, self.help_command)

        _clear_command_info: CommandInfo = CommandInfo(name='clear', description='Clears the screen.',
                                                       usage='\tclear - Clears the screen.')
        _clear_command: Command = Command('clear', _clear_command_info, self.clear_command)

        _ls_command_info: CommandInfo = CommandInfo(name='ls', description='Lists the contents of a directory.',
                                                    usage='\tls <directory> - Lists the contents of a directory.')
        _ls_command: Command = Command('ls', _ls_command_info, self.ls_command)

        _cd_command_info: CommandInfo = CommandInfo(name='cd', description='Changes the current directory.',
                                                    usage='\tcd <directory> - Changes the current directory.')
        _cd_command: Command = Command('cd', _cd_command_info, self.cd_command)

        _os_info_command_info: CommandInfo = CommandInfo(name='osinfo', description='Displays the OS info.',
                                                         usage='\tname - Displays the operating system info.')
        _os_info_command: Command = Command('osinfo', _os_info_command_info, self.osinfo_command)

        _python_command_info: CommandInfo = CommandInfo(name='python', description='Runs a Python script.',
                                                        usage='\tpython <script> - Runs a Python script.',
                                                        needs_root=True)
        _python_command: Command = Command('python', _python_command_info, self.python_command)

        _power_off_command_info: CommandInfo = CommandInfo(name='poweroff',
                                                           description='Shutdowns the operating system.',
                                                           usage='\tpoweroff - Shutdowns the operating system.',
                                                           needs_root=True)
        _power_off_command: Command = Command('poweroff', _power_off_command_info, self.poweroff_command)

        _cat_command_info: CommandInfo = CommandInfo(name='cat', description='Displays the contents of a file.',
                                                     usage='\tcat <file> - Displays the contents of a file.')
        _cat_command: Command = Command('cat', _cat_command_info, self.cat_command)

        _rm_command_details: CommandInfo = CommandInfo(name='rm', description='Removes a file or directory.',
                                                       usage='\trm <file> - Removes a file or directory.',
                                                       needs_root=True)
        _rm_command: Command = Command('rm', _rm_command_details, self.rm_command)

        _source_command_details: CommandInfo = CommandInfo(name='source', description='Displays the source module of a '
                                                                                      'command',
                                                           usage='\tsource <command> - Displays the source module of a '
                                                                 'command', needs_root=False)
        _source_command: Command = Command('source', _source_command_details, self.source_command)

        _module_command_details: CommandInfo = CommandInfo(name='module', description='Displays information about a '
                                                                                      'module',
                                                           usage='\tmodule <module> - Displays information about a '
                                                                 'module\n\tmodule -a - Displays all the modules '
                                                                 'currently active on the system.\n\tmodule <module> '
                                                                 '-rm - Removes a module from the system.',
                                                           needs_root=False)
        _module_command: Command = Command('module', _module_command_details, self.module_command)

        _bash_command_details: CommandInfo = CommandInfo(name='bash', description='Runs a bash script.',
                                                            usage='\tbash <script> - Runs a bash script.',
                                                            needs_root=False)
        _bash_command: Command = Command('bash', _bash_command_details, self.bash_command)

        _echo_commands_details: CommandInfo = CommandInfo(name='echo', description='Prints a message.',
                                                            usage='\techo <message> - Prints a message.',
                                                            needs_root=False)
        _echo_command: Command = Command('echo', _echo_commands_details, self.echo_command)

        # Add commands to the list.
        self.commands[_help_command.keyword] = _help_command
        self.commands[_clear_command.keyword] = _clear_command
        self.commands[_ls_command.keyword] = _ls_command
        self.commands[_cd_command.keyword] = _cd_command
        self.commands[_os_info_command.keyword] = _os_info_command
        self.commands[_python_command.keyword] = _python_command
        self.commands[_power_off_command.keyword] = _power_off_command
        self.commands[_cat_command.keyword] = _cat_command
        self.commands[_rm_command.keyword] = _rm_command
        self.commands[_source_command.keyword] = _source_command
        self.commands[_module_command.keyword] = _module_command
        self.commands[_bash_command.keyword] = _bash_command
        self.commands[_echo_command.keyword] = _echo_command

        self.load_module_commands()

    def run(self, args: list, as_admin: bool) -> str:
        for command in self.commands.values():
            if command.keyword == args[0]:
                if command.info.needs_root and not as_admin:
                    return 'You need to be root to run this command.'
                else:
                    if command.info.needs_fs:
                        return command.invoke(args=args[1:], as_root=as_admin, file_system=self.file_system)
                    else:
                        return command.invoke(args=args[1:], as_root=as_admin)

        return f'Command not found: "{args[0]}".'

    def load_module_commands(self):
        """Loads the commands from the modules."""
        self.module_loader.initialize()

        module_commands: list = self.module_loader.get_module_commands()

        for command in module_commands:
            module = command['module']
            command = command['command']

            command_info: CommandInfo = CommandInfo(name=command['name'], description=command['description'],
                                                    usage=command['usage'], needs_root=command['needs_root'],
                                                    source_module=module, needs_fs=command['needs_fs'])
            command: Command = Command(command['keyword'], command_info, command['function'])

            if command.keyword not in self.commands:
                self.commands[command.keyword] = command
            else:
                self.logger.log(f'Command {command.keyword} already exists.', Priority.HIGH)

    ##############################

    def help_command(self, args: list, as_admin: bool) -> str:
        if len(args) == 0:
            return str(self.commands['help'].info) + f'\n\tNeeds Root: {self.commands["help"].info.needs_root}'
        else:
            if args[0] == '-a':
                return_str: str = ''

                for command in self.commands.values():
                    return_str += f'{command.info}\n\tNeeds Root: {command.info.needs_root}\n\n'

                return_str = return_str.rstrip('\n\n')

                return return_str
            else:
                if args[0] in self.commands:
                    return str(
                        self.commands[args[0]].info) + f'\n\tNeeds Root: {self.commands[args[0]].info.needs_root}'
                else:
                    return f'Command not found: {args[0]}'

    def clear_command(self, args: list, as_admin: bool) -> str:
        # Clear the screen.
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        return ''

    def ls_command(self, args: list, as_admin: bool) -> str:
        return self.file_system.list_cwd()

    def cd_command(self, args: list, as_admin: bool) -> str:
        if len(args) == 0:
            return 'Please specify a directory.'
        else:
            return self.file_system.change_dir(Path(args[0]))

    def osinfo_command(self, args: list, as_admin: bool) -> str:
        return self.os_info

    def python_command(self, args: list, as_admin: bool) -> str:
        if len(args) == 0:
            return 'Please specify a script.'
        else:
            return self.file_system.run_python_script(args[0])

    def poweroff_command(self, args: list, as_admin: bool):
        if as_admin:
            quit()

    def cat_command(self, args: list, as_admin: bool) -> str:
        if len(args) == 0:
            return 'Please specify a file.'
        else:
            return self.file_system.cat_file(args[0])

    def rm_command(self, args: list, as_admin: bool) -> str:
        if len(args) == 0:
            return 'Please specify a file or directory.'
        else:
            return self.file_system.rm_item(args[0], ('-y' in args))

    def source_command(self, args: list, as_admin: bool) -> str:
        if len(args) == 0:
            return 'Please specify a command.'
        else:
            command = args[0]

            if command in self.commands:
                if self.commands[args[0]].info.source_module == '':
                    return f'Command: "{command}" is a built-in command.'
                else:
                    source_module = self.commands[args[0]].info.source_module
                    return f'Command: "{command} "is from module: "{source_module}".\nRun "module {source_module}" for ' \
                           f'more information on the module.'
            else:
                return f'Command not found: "{args[0]}".'

    def module_command(self, args: list, as_admin: bool) -> str:
        if len(args) == 0:
            return 'Please specify a module.'
        else:
            result, commands_to_remove = self.module_loader.module_command(args=args, as_admin=as_admin)

            for command in commands_to_remove:
                if command['keyword'] in self.commands:
                    del self.commands[command['keyword']]
                    result = f'Removed command: "{command["keyword"]}".\n{result}'

            return result

    def bash_command(self, args: list, as_admin: bool) -> str:
        if len(args) == 0:
            return 'Please specify a file.'
        else:
            error, lines = self.file_system.get_file_lines(args[0])

            if error != '':
                return error
            else:
                for line in lines:
                    if not line.strip() == '':
                        lexer: Lexer = Lexer(text=line.strip(), logger=self.logger)  # Create a lexer.
                        tokens = lexer.lex()

                        if len(tokens) > 0:
                            as_admin: bool = False

                            if tokens[0] == 'sudo':
                                as_admin = True
                                tokens.pop(0)

                            output = self.run(args=tokens, as_admin=as_admin)

                            if not output == '' and output is not None and str(output) != 'None':
                                print(output)

                        self.run(args=tokens, as_admin=as_admin)

                return ''

    def echo_command(self, args: list, as_admin: bool) -> str:
        return ''.join(args)
