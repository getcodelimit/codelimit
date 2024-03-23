from codelimit.common.Token import Token
from codelimit.common.token_matching.Matcher import TokenPredicate
from codelimit.common.token_matching.predicates.Value import Value


class Balanced(TokenPredicate):
    def __init__(self, left: str | TokenPredicate, right: str | TokenPredicate):
        super().__init__()
        self.left = left if isinstance(left, TokenPredicate) else Value(left)
        self.right = right if isinstance(right, TokenPredicate) else Value(right)
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
