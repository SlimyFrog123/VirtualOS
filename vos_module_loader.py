##############################
# IMPORTS
##############################


import os
import sys
from vos_logger import Logger
from vos_priority import Priority


##############################
# VARIABLES
##############################


MODULE_FOLDER: str = 'modules'


##############################
# MODULE LOADER
##############################


class ModuleLoader:
    def __init__(self, logger: Logger, module_folder: str = None):
        if module_folder is not None:
            self.module_folder: str = module_folder
        else:
            self.module_folder: str = MODULE_FOLDER

        self.modules: list = list()
        self.logger: Logger = logger

    def initialize(self):
        self.logger.log('Loading modules...')

        if not os.path.exists(self.module_folder):
            os.mkdir(self.module_folder)

            with open(self.module_folder + os.sep + '__init__.py', 'w') as f:
                f.write('')
        else:
            if not os.path.exists(self.module_folder + os.sep + '__init__.py'):
                with open(self.module_folder + os.sep + '__init__.py', 'w') as f:
                    f.write('')

        for item in os.scandir(self.module_folder):
            if item.is_file():
                if item.name.endswith('.py') and not item.name.startswith('__'):
                    module_file_name_no_ext: str = item.name.replace('.py', '')
                    module_file_name: str = item.name

                    try:
                        module = __import__(f'{self.module_folder}.{module_file_name_no_ext}',
                                            fromlist=[module_file_name_no_ext])
                        self.modules.append(module.module)

                        self.logger.log(f'Loaded module: "{module.module["name"]}".', Priority.NONE)
                    except Exception as e:
                        self.logger.log(f'Failed to load module: "{module_file_name}".', Priority.HIGH)
                        self.logger.log(f'Error: {e}.', Priority.HIGH)

    def get_module_commands(self) -> list:
        """Load the commands from all modules."""
        commands: list = list()

        # Get every command from every module and add it to the list.
        for module in self.modules:
            for command in module['commands']:
                commands.append({'command': module['commands'][command], 'module': module['name']})

        return commands

    def module_command(self, args: list, as_admin: bool) -> tuple[str, list]:
        module = None

        if args[0] == '-a':
            modules_string: str = ''

            for module in self.modules:
                modules_string += f'{module["name"]}\n'

            if len(self.modules) == 0:
                return 'No modules currently loaded.', list()

            return f'Modules:\n{modules_string}'.rstrip('\n'), list()

        for _module in self.modules:
            if _module['name'] == args[0]:
                module = _module
                break

        if module is not None:
            if len(args) == 1:
                module_name = module['name']
                module_description = module['description']
                module_version = module['version']
                module_author = module['author']

                return f'{module_name}\n' \
                       f'{module_description}\n' \
                       f'Author: {module_author}\t Version: {module_version}', list()
            elif '-rm' in args:
                if as_admin:
                    sys.modules.pop(f'{self.module_folder}.{module["name"]}')
                    commands_from_module: list = list()

                    for command in module['commands']:
                        commands_from_module.append(module['commands'][command])

                    self.modules.remove(module)

                    return f'Removed module: {module["name"]}', commands_from_module
                else:
                    return 'You must have root privileges to remove a module.', list()
        else:
            return 'Module not found, use "module -a" to list all modules.', list()
