from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate
from codelimit.common.token_matching.predicates.Value import Value


class Optional(TokenPredicate):
    def __init__(self, item: TokenPredicate | str):
        super().__init__()
        self.satisfied = True
        self._predicate = item if isinstance(item, TokenPredicate) else Value(item)

    def reset(self):
        self._predicate.reset()

    def accept(self, token) -> bool:
        if self._predicate.satisfied:
            return False
        return self._predicate.accept(token)
