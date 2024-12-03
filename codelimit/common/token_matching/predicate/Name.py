from codelimit.common.Token import Token
from codelimit.common.token_matching.predicate.TokenPredicate import TokenPredicate


class Name(TokenPredicate):
    def accept(self, token: Token) -> bool:
        if token.is_name():
            self.satisfied = True
            return True
        return False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Name)

    def __hash__(self):
        return hash("Name")

    def __str__(self):
        return "<Name>"
