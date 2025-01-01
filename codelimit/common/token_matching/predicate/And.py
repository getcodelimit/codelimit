from codelimit.common.Token import Token
from codelimit.common.token_matching.predicate.TokenPredicate import TokenPredicate
from codelimit.common.token_matching.predicate.TokenValue import TokenValue


class And(TokenPredicate):
    def __init__(self, left: str | TokenPredicate, right: str | TokenPredicate):
        super().__init__()
        self.left = left if isinstance(left, TokenPredicate) else TokenValue(left)
        self.right = right if isinstance(right, TokenPredicate) else TokenValue(right)

    def accept(self, token: Token) -> bool:
        return self.left.accept(token) and self.right.accept(token)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, And):
            return False
        return self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.left, self.right))
