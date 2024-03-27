from codelimit.common.Token import Token
from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate


class Value(TokenPredicate):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def accept(self, token: Token) -> bool:
        if token.value == self.value:
            self.satisfied = True
            return True
        return False
