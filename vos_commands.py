##############################
# COMMAND INFO
##############################


class CommandInfo:
    def __init__(self, name: str, description: str, usage: str, needs_root: bool = False, source_module: str = '', needs_fs: bool = False):
        self.name = name
        self.description = description
        self.usage = usage
        self.needs_root = needs_root
        self.source_module = source_module
        self.needs_fs = needs_fs

    def __repr__(self):
        if self.needs_root:
            pass

        return f'{self.name} - {self.description}\nUsage:\n{self.usage}'


##############################
# COMMAND
##############################


class Command:
    def __init__(self, keyword: str, info: CommandInfo, function: callable):
        self.keyword = keyword
        self.info = info
        self.function = function

    def invoke(self, args: list, as_root: bool = False, file_system = None) -> str:
        if self.info.needs_root and not as_root:
            return 'You need to be root to run this command.'

        if file_system is not None:
            return self.function(args, as_root, file_system)
        else:
            return self.function(args, as_root)
