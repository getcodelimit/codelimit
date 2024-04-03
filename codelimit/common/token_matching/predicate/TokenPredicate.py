from abc import abstractmethod

from codelimit.common.Token import Token
from codelimit.common.gsm.predicate.Predicate import Predicate


class TokenPredicate(Predicate[Token]):
    def __init__(self):
        self.satisfied = False

    def reset(self):
        self.satisfied = False

    @abstractmethod
    def accept(self, token: Token) -> bool:
        pass
