from abc import ABC, abstractmethod

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange


class ScopeExtractor(ABC):

    @abstractmethod
    def extract_headers(self, tokens: list[Token]) -> list[TokenRange]:
        pass

    @abstractmethod
    def extract_blocks(self, tokens: list[Token]) -> list[TokenRange]:
        pass
