from codelimit.common.Token import Token
from codelimit.common.token_matching.predicate.TokenPredicate import TokenPredicate


class Operator(TokenPredicate):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def accept(self, token: Token) -> bool:
        if token.is_operator(self.symbol):
            self.satisfied = True
            return True
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Operator):
            return False
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)
