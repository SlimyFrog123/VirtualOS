# VirtualOS
Virtual "OS" made in Python.

This is just a simple attempt at making a sort-of "OS" in Python.  It's not an actual operating system, only a simulation of one, running in Python with its own filesystem and files.
The files from it are actually on your device, and you can view them.  They are in a folder called vos_fs, which will be wherever you ran the python file, that is the root directory of the filesystem.

Installation
------------

The installation process is quite simple, all you need is Python 3, git, and pip installed.

First, clone the repository.
`git clone https://github.com/SlimyFrog123/VirtualOS.git`

Then, install the required dependencies:
 - `pip install art`
 - `pip install pathlib`
 - `pip install requests`
 - `pip install colorama`
 - `pip install tqdm`

Then, run `virtual_os.py` after installing the dependencies:
`python3 virtual_os.py`

Credits
-------

Thank you to everyone that I have used code from, this wouldn't have been possible without you!

Used in the project:
 - https://github.com/davidcallanan/py-myopl-code/ - Code for the BASIC interpreter module (tweaked a bit to fit the needs of the project).
