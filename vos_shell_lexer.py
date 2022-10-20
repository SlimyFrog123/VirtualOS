##############################
# IMPORTS
##############################


import string
from vos_logger import Logger
from vos_priority import Priority


##############################
# LEXER
##############################


class Lexer:
    def __init__(self, text, logger: Logger):
        self.text: str = text
        self.logger: Logger = logger
        self.pos: int = -1
        self.current_char = self.text[self.pos]
        self.tokens: list = list()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def lex(self) -> list:
        self.tokens = []

        while self.current_char is not None:
            self.advance()

            if self.current_char == '"':
                self.tokens.append(self.make_string())
            elif self.current_char not in string.whitespace:
                self.tokens.append(self.make_token())
            else:
                self.advance()

        # Remove all empty tokens.
        while '' in self.tokens:
            self.tokens.remove('')

        return self.tokens

    def make_string(self) -> str:
        return_str: str = ''
        self.advance()

        while self.current_char != '"' and self.current_char is not None:
            return_str += self.current_char
            self.advance()

        if self.current_char != '"':
            self.logger.log('Expected closing quote.', Priority.HIGH)
            return ''

        self.advance()

        return return_str

    def make_token(self) -> str:
        return_str: str = ''

        while self.current_char is not None and self.current_char not in string.whitespace:
            return_str += self.current_char
            self.advance()

        return return_str
