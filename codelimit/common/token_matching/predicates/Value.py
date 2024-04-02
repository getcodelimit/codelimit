from typing import TypeVar

from codelimit.common.Token import Token
from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate

T = TypeVar('T')


class Value(TokenPredicate):
    def __init__(self, value: T):
        super().__init__()
        self.value = value

    def accept(self, token: Token) -> bool:
        if token.value == str(self.value):
            self.satisfied = True
            return True
        return False
