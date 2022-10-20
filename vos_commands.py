##############################
# COMMAND INFO
##############################


class CommandInfo:
    def __init__(self, name: str, description: str, usage: str, needs_root: bool = False):
        self.name = name
        self.description = description
        self.usage = usage
        self.needs_root = needs_root

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

    def invoke(self, args: list, as_root: bool = False) -> str:
        if self.info.needs_root and not as_root:
            return 'You need to be root to run this command.'

        return self.function(args, as_root)
