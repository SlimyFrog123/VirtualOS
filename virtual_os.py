##############################
# IMPORTS
##############################


import sys
from vos_logger import Logger
from vos_kernel import Kernel
from vos_file_system import FileSystem
from vos_shell import Shell

##############################
# MAIN PROGRAM
##############################


if __name__ == '__main__':
    logger: Logger = Logger()  # Create a logger.
    file_system: FileSystem = FileSystem(logger)  # Create a file system.
    shell: Shell = Shell(file_system=file_system, logger=logger)  # Create a shell.
    kernel: Kernel = Kernel(name='Virtual OS', version='1.0', release='1', build='1', architecture='x86_64',
                            file_system=file_system, logger=logger, shell=shell)  # Create a kernel.

    kernel.initialize()  # Initialize the kernel.
    kernel.boot()  # Boot the kernel.
