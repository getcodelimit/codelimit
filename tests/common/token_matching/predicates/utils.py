from pygments.token import Punctuation, Keyword, Operator

from codelimit.common.Location import Location
from codelimit.common.Token import Token


def symbol_token(value: str) -> Token:
    return Token(Location(1, 1), Punctuation, value)

def keyword_token(value: str) -> Token:
    return Token(Location(1, 1), Keyword, value)

def operator_token(value: str) -> Token:
    return Token(Location(1, 1), Operator, value)
