from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate


class Optional(TokenPredicate):
    def __init__(self, predicate: TokenPredicate):
        super().__init__()
        self.satisfied = True
        self._predicate = predicate

    def reset(self):
        self._predicate.reset()

    def accept(self, token) -> bool:
        if self._predicate.satisfied:
            return False
        return self._predicate.accept(token)
