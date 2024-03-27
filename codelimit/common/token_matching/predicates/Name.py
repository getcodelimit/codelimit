from codelimit.common.Token import Token
from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate


class Name(TokenPredicate):
    def accept(self, token: Token) -> bool:
        if token.is_name():
            self.satisfied = True
            return True
        return False
