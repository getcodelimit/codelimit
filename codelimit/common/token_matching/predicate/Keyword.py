from codelimit.common.Token import Token
from codelimit.common.token_matching.predicate.TokenPredicate import TokenPredicate


class Keyword(TokenPredicate):
    def __init__(self, keyword: str):
        super().__init__()
        self.keyword = keyword

    def accept(self, token: Token) -> bool:
        if token.is_keyword() and token.value == self.keyword:
            self.satisfied = True
            return True
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Keyword):
            return False
        return self.keyword == other.keyword

    def __hash__(self):
        return hash(self.keyword)

    def __str__(self):
        return f"<Keyword {self.keyword}>"
