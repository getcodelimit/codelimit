from pygments.token import Keyword, Text, Whitespace, Comment, Punctuation, Name

from codelimit.common.SourceLocation import SourceLocation


class Token:
    def __init__(self, location: SourceLocation, type: any, value: str):
        self.location = location
        self.type = type
        self.value = value

    def is_keyword(self):
        return self.type in Keyword

    def is_whitespace(self):
        return (self.type == Text or self.type == Whitespace) and self.value.isspace()

    def is_comment(self):
        return self.type in Comment

    def is_symbol(self, symbol: str):
        return self.type in Punctuation and self.value == symbol

    def is_name(self):
        return self.type in Name

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)