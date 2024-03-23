from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate
from codelimit.common.token_matching.predicates.Value import Value


class Lookahead(TokenPredicate):
    def __init__(self, item: TokenPredicate | str):
        super().__init__()
        predicate = item if isinstance(item, TokenPredicate) else Value(item)
        self.__dict__ = predicate.__dict__
        self._predicate = predicate

    def accept(self, token) -> bool:
        return self._predicate.accept(token)
