from codelimit.common.Token import Token
from codelimit.common.token_matching.Matcher import TokenPredicate


class Keyword(TokenPredicate):
    def __init__(self, keyword: str):
        super().__init__()
        self.keyword = keyword

    def accept(self, token: Token) -> bool:
        if token.is_keyword() and token.value == self.keyword:
            self.satisfied = True
            return True
        return False
