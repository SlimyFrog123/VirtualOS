##############################
# IMPORTS
##############################


import os
from vos_commands import Command, CommandInfo
from vos_file_system import FileSystem, Path


##############################
# SHELL COMMANDS
##############################


class ShellCommands:
    def __init__(self, file_system: FileSystem, os_info: str):
        self.commands: dict = {}
        self.file_system: FileSystem = file_system
        self.os_info = os_info
        self.initialize()

    def initialize(self):
        """Initializes the shell commands."""
        _help_command_info: CommandInfo = CommandInfo(name='help', description='Displays help for a command.',
                                                      usage='\thelp [command] - Displays help for a specific '
                                                            'command.\n\thelp -a - Displays help for all commands.')
        _help_command: Command = Command('help', _help_command_info, self.help_command)

        _clear_command_info: CommandInfo = CommandInfo(name='clear', description='Clears the screen.',
                                                       usage='\tclear - Clears the screen.')
        _clear_command: Command = Command('clear', _clear_command_info, self.clear_command)

        _ls_command_info: CommandInfo = CommandInfo(name='ls', description='Lists the contents of a directory.',
                                                    usage='\tls [directory] - Lists the contents of a directory.')
        _ls_command: Command = Command('ls', _ls_command_info, self.ls_command)

        _cd_command_info: CommandInfo = CommandInfo(name='cd', description='Changes the current directory.',
                                                    usage='\tcd [directory] - Changes the current directory.')
        _cd_command: Command = Command('cd', _cd_command_info, self.cd_command)

        _os_info_command_info: CommandInfo = CommandInfo(name='osinfo', description='Displays the OS info.',
                                                         usage='\tname - Displays the operating system info.')
        _os_info_command: Command = Command('osinfo', _os_info_command_info, self.osinfo_command)

        _python_command_info: CommandInfo = CommandInfo(name='python', description='Runs a Python script.',
                                                        usage='\tpython [script] - Runs a Python script.',
                                                        needs_root=True)
        _python_command: Command = Command('python', _python_command_info, self.python_command)

        _poweroff_command_info: CommandInfo = CommandInfo(name='poweroff', description='Shutdowns the operating system.',
                                                            usage='\tpoweroff - Shutdowns the operating system.',
                                                            needs_root=True)
        _poweroff_command: Command = Command('poweroff', _poweroff_command_info, self.poweroff_command)

        _cat_command_info: CommandInfo = CommandInfo(name='cat', description='Displays the contents of a file.',
                                                            usage='\tcat [file] - Displays the contents of a file.')
        _cat_command: Command = Command('cat', _cat_command_info, self.cat_command)

        _rm_command_details: CommandInfo = CommandInfo(name='rm', description='Removes a file or directory.',
                                                       usage='\trm [file] - Removes a file or directory.', needs_root=True)
        _rm_command: Command = Command('rm', _rm_command_details, self.rm_command)

        # Add commands to the list.
        self.commands[_help_command.keyword] = _help_command
        self.commands[_clear_command.keyword] = _clear_command
        self.commands[_ls_command.keyword] = _ls_command
        self.commands[_cd_command.keyword] = _cd_command
        self.commands[_os_info_command.keyword] = _os_info_command
        self.commands[_python_command.keyword] = _python_command
        self.commands[_poweroff_command.keyword] = _poweroff_command
        self.commands[_cat_command.keyword] = _cat_command
        self.commands[_rm_command.keyword] = _rm_command

    def run(self, args: list, as_admin: bool) -> str:
        for command in self.commands.values():
            if command.keyword == args[0]:
                if command.info.needs_root and not as_admin:
                    return 'You need to be root to run this command.'
                else:
                    return command.invoke(args[1:], as_admin)

        return f'Command not found: {args[0]}'

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
                    return str(self.commands[args[0]].info) + f'\n\tNeeds Root: {self.commands[args[0]].info.needs_root}'
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
