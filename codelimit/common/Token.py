from typing import Any

from pygments.token import (
    Keyword,
    Text,
    Whitespace,
    Comment,
    Punctuation,
    Operator,
    Name,
)

from codelimit.common.Location import Location


class Token:
    def __init__(self, location: Location, token_type: Any, value: str):
        self.location = location
        self.token_type = token_type
        self.value = value

    def is_keyword(self):
        return self.token_type in Keyword

    def is_whitespace(self):
        return (
            self.token_type == Text or self.token_type == Whitespace
        ) and self.value.isspace()

    def is_comment(self):
        return self.token_type in Comment

    def is_symbol(self, symbol: str):
        return self.token_type in Punctuation and self.value == symbol

    def is_operator(self, symbol: str):
        return self.token_type in Operator and self.value == symbol

    def is_name(self):
        return self.token_type in Name

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented

        return (
            self.location == other.location
            and str(self.token_type) == str(other.token_type)
            and self.value == other.value
        )
