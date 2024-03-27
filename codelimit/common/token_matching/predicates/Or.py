from codelimit.common.Token import Token
from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate
from codelimit.common.token_matching.predicates.Value import Value


class Or(TokenPredicate):
    def __init__(self, left: str | TokenPredicate, right: str | TokenPredicate):
        super().__init__()
        self._left = left if isinstance(left, TokenPredicate) else Value(left)
        self._right = right if isinstance(right, TokenPredicate) else Value(right)

    def accept(self, token: Token) -> bool:
        if self._left.accept(token) or self._right.accept(token):
            self.satisfied = True
            return True
        return False
