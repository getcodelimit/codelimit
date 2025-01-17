from codelimit.common.Token import Token
from codelimit.common.token_matching.predicate.TokenPredicate import TokenPredicate


class TokenValue(TokenPredicate):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def accept(self, token: Token) -> bool:
        if token.value == self.value:
            self.satisfied = True
            return True
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TokenValue):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return self.value
