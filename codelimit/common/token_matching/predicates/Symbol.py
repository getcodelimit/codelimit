from codelimit.common.Token import Token
from codelimit.common.token_matching.Matcher import TokenPredicate


class Symbol(TokenPredicate):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def accept(self, token: Token) -> bool:
        if token.is_symbol(self.symbol):
            self.satisfied = True
            return True
        return False
