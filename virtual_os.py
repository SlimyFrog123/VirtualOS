##############################
# IMPORTS
##############################


import sys
import time
from vos_logger import Logger
from vos_priority import Priority
from vos_kernel import Kernel
from vos_file_system import FileSystem, Path
from vos_shell import Shell

##############################
# MAIN PROGRAM
##############################


if __name__ == '__main__':
    is_internal: bool = not ('--external' in sys.argv)  # Check if the program is running internally or externally.

    logger: Logger = Logger(is_internal)  # Create a logger.
    file_system: FileSystem = FileSystem()  # Create a file system.
    shell: Shell = Shell(file_system=file_system, logger=logger)  # Create a shell.
    kernel: Kernel = Kernel(name='Virtual OS', version='1.0', release='1', build='1', architecture='x86_64',
                            file_system=file_system, logger=logger, shell=shell)  # Create a kernel.

    kernel.initialize()  # Initialize the kernel.
    kernel.boot()  # Boot the kernel.
