from codelimit.common.Token import Token
from codelimit.common.token_matching.predicate.TokenPredicate import TokenPredicate
from codelimit.common.token_matching.predicate.TokenValue import TokenValue


class Balanced(TokenPredicate):
    def __init__(self, left: str | TokenPredicate, right: str | TokenPredicate):
        super().__init__()
        self.left = left if isinstance(left, TokenPredicate) else TokenValue(left)
        self.right = right if isinstance(right, TokenPredicate) else TokenValue(right)
        self.depth = 0

    def reset(self):
        super().reset()
        self.left.reset()
        self.right.reset()
        self.depth = 0

    def accept(self, token: Token) -> bool:
        if self.left.accept(token):
            self.depth += 1
            return True
        elif self.right.accept(token):
            self.depth -= 1
            if self.depth < 0:
                return False
            if self.depth == 0:
                self.satisfied = True
            return True
        else:
            return self.depth > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Balanced):
            return False
        return (
            self.left == other.left
            and self.right == other.right
            and self.depth == other.depth
        )

    def __hash__(self):
        return hash((self.left, self.right, self.depth))

    def __str__(self):
        return f"<Balanced {self.left} {self.right} {id(self)}>"
