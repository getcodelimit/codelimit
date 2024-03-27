from abc import ABC, abstractmethod

from codelimit.common.Token import Token


class TokenPredicate(ABC):
    def __init__(self):
        self.satisfied = False

    def reset(self):
        self.satisfied = False

    @abstractmethod
    def accept(self, token: Token) -> bool:
        pass
