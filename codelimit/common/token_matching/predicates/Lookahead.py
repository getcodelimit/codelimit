from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate


class Lookahead(TokenPredicate):
    def __init__(self, predicate: TokenPredicate):
        super().__init__()
        self.__dict__ = predicate.__dict__
        self._predicate = predicate

    def accept(self, token) -> bool:
        return self._predicate.accept(token)
