##############################
# IMPORTS
##############################


import os
import sys
import requests
import urllib.request
from vos_logger import Logger
from vos_priority import Priority
from vos_file_system import FileSystem, Path


##############################
# VARIABLES
##############################


MODULE_FOLDER: str = 'modules'
APT_ENDPOINT: str = 'https://virtualos-apt.slimyfrog123.repl.co/api/'


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
        self.commands_to_remove: list = list()

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
            if item.is_file() and item.name.endswith('.py') and not item.name == '__init__.py':
                module_file_name_no_ext: str = item.name.replace('.py', '')
                module_file_name: str = item.name

                if f'{self.module_folder}.{module_file_name_no_ext}' in sys.modules:
                    continue

                try:
                    module = __import__(f'{self.module_folder}.{module_file_name_no_ext}',
                                        fromlist=[module_file_name_no_ext])

                    module_details = module.module
                    module_details['__name__'] = module_file_name_no_ext

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
                modules_string += f'{module["__name__"]}\n'

            if len(self.modules) == 0:
                return 'No modules currently loaded.', list()

            return f'Modules:\n{modules_string}'.rstrip('\n'), list()

        for _module in self.modules:
            if _module['__name__'] == args[0]:
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
                    sys.modules.pop(f'{self.module_folder}.{module["__name__"]}')
                    commands_from_module: list = list()

                    for command in module['commands']:
                        commands_from_module.append(module['commands'][command])

                    self.modules.remove(module)

                    return f'Removed module: {module["name"]}', commands_from_module
                else:
                    return 'You must have root privileges to remove a module.', list()
        else:
            return 'Module not found, use "module -a" to list all modules.', list()

    def module_exists(self, module_name: str) -> bool:
        for module in self.modules:
            if module['__name__'] == module_name:
                return True

        return False

    def get_module(self, module_name: str):
        module = None

        for _module in self.modules:
            if _module['__name__'] == module_name:
                module = _module
                break

        if module is not None:
            return module

        return None

    def apt_command(self, args: list, as_admin: bool, file_system: FileSystem) -> str:
        if args[0] == 'upgrade':
            pass  # Upgrade all modules.

        if len(args) > 1:
            if args[0] == 'install':
                if self.module_exists(args[1]):
                    return 'Module already installed.'
                else:
                    try:
                        response = requests.get(APT_ENDPOINT + 'package/' + str(args[1]))
                        res = response.json()

                        if res['status'] == 'ok':
                            self.logger.log(f'Package found: "{res["package"]["name"]}" ({str(args[1])})')
                            self.logger.log('Attempting download...')

                            try:
                                download_url = res['package']['download_url']
                                module_filename = res['package']['filename']

                                modules_path = file_system.root.as_local.path.replace(os.sep + 'vos_fs', os.sep +
                                                                                      'modules')

                                # urllib.request.urlretrieve(download_url, os.path.join(modules_path, module_filename))

                                content = requests.get(download_url).text
                                with open(os.path.join(modules_path, module_filename), 'w') as file:
                                    file.write(content)

                                self.logger.log(f'Successfully downloaded package: "{res["package"]["name"]}"! '
                                                f'Reloading modules...')

                                self.initialize()  # Reload the modules/packages.

                                self.logger.log('Package installation succeeded!')

                                return 'reload_packages'
                            except Exception as e:
                                return f'Download failed due to Error:\n\t{e}'
                        else:
                            return 'Package does not exist!'
                    except Exception as e:
                        return f'Operation Failed due to Error:\n\t{e}'
            elif args[0] == 'remove':
                modules_path = file_system.root.as_local.path.replace(os.sep + 'vos_fs', os.sep + 'modules')
                if self.module_exists(args[1]):
                    module = self.get_module(str(args[1]))
                    os.remove(os.path.join(modules_path, str(args[1]) + '.py'))

                    result, commands_to_remove = self.module_command([module['__name__'], '-rm'], True)

                    self.commands_to_remove = commands_to_remove

                    return 'reload_packages_and_commands'
                else:
                    return 'Package not found.'
            elif args[0] == 'update':
                if self.module_exists(str(args[1])):
                    pac = self.get_module(str(args[1]))

                    if pac is None:
                        return 'Unknown error occurred.'
                    else:
                        package_version = str(pac['version'])
                        package_server_version: str = ''

                        try:
                            response = requests.get(APT_ENDPOINT + 'package/' + str(pac['__name__']))
                            res = response.json()

                            if res['status'] == 'ok':
                                package_server_version = str(res['package']['version'])

                                if package_version != package_server_version:
                                    try:
                                        download_url = res['package']['download_url']
                                        module_filename = res['package']['filename']
                                        modules_path = file_system.root.as_local.path.replace(os.sep + 'vos_fs',
                                                                                              os.sep + 'modules')
                                        fp = os.path.join(modules_path, module_filename)

                                        os.remove(fp)
                                        # urllib.request.urlretrieve(download_url, fp)

                                        content = requests.get(download_url).text
                                        with open(fp, 'w') as file:
                                            file.write(content)

                                        self.logger.log(f'Successfully downloaded package: "{res["package"]["name"]}"! '
                                                        f'Reloading modules...')

                                        self.initialize()  # Reload the modules/packages.

                                        self.logger.log('Package successfully updated!')
                                    except Exception as e:
                                        return f'Download failed due to Error:\n\t{e}'

                                    module = self.get_module(str(res['package']['filename']).rstrip('.py'))

                                    if module is not None:
                                        result, commands_to_remove = self.module_command(args=[module['__name__'],
                                                                                               '-rm'], as_admin=True)

                                        self.commands_to_remove = commands_to_remove

                                        return 'reload_packages_and_commands'
                                else:
                                    return f'Package is already up-to-date!'
                            else:
                                return 'Unknown error occurred.'
                        except Exception as e:
                            return f'Operation Failed due to Error:\n\t{e}'
                else:
                    return 'Package not found.'
            elif args[0] == 'info':
                if self.module_exists(str(args[1])):
                    module = self.get_module(str(args[1]))
                    result, commands_to_remove = self.module_command([module['__name__']], True)

                    return result
                else:
                    return 'Package not found.'
        else:
            return 'Usage: apt <command> <package>.'
