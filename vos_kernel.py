##############################
# IMPORTS
##############################


import art
from vos_file_system import FileSystem
from vos_logger import Logger
from vos_priority import Priority
from vos_shell import Shell


##############################
# KERNEL
##############################


class Kernel:
    def __init__(self, name: str, version: str, build: str, release: str, architecture: str, file_system: FileSystem,
                 logger: Logger, shell: Shell):
        self.name: str = name
        self.version: str = version
        self.build: str = build
        self.release: str = release
        self.architecture: str = architecture
        self.file_system: FileSystem = file_system
        self.logger: Logger = logger
        self.shell: Shell = shell

    def __repr__(self):
        return f'Kernel(name={self.name}, version={self.version}, build={self.build}, release={self.release}, ' \
               f'architecture={self.architecture})'

    def initialize(self):
        # Initialize all the components of the kernel.
        self.file_system.initialize()  # Initialize the file system.
        self.shell.initialize(self.info_str)

    @property
    def info_str(self):
        return f'{self.name} v{self.version} ({self.architecture})'

    def boot(self):
        print(art.text2art(self.name))  # Print the name of the OS.
        # Print the OS details.
        print(f'Version: v{self.version}\tBuild: {self.build}\tRelease: {self.release}\tArch: {self.architecture}')

        self.logger.log('Kernel booted successfully.', Priority.LOW)  # Log that the kernel booted successfully.
        self.shell.run()  # Run the shell.
