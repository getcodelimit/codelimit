from codelimit.common.Token import Token
from codelimit.common.token_matching.predicate.TokenPredicate import TokenPredicate
from codelimit.common.token_matching.predicate.TokenValue import TokenValue


class Not(TokenPredicate):
    def __init__(self, value: TokenPredicate | str):
        super().__init__()
        self.predicate = value if isinstance(value, TokenPredicate) else TokenValue(value)

    def accept(self, token: Token) -> bool:
        return not self.predicate.accept(token)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Not):
            return False
        return self.predicate == other.predicate

    def __hash__(self):
        return hash(self.predicate)
