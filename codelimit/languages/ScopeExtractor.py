from abc import ABC, abstractmethod

from codelimit.common.SourceRange import SourceRange
from codelimit.common.Token import Token


class ScopeExtractor(ABC):
    @abstractmethod
    def extract_blocks(self, code: str, tokens: list[Token]) -> list[SourceRange]:
        pass

    @abstractmethod
    def extract_headers(self, code: str, tokens: list[Token]) -> list[SourceRange]:
        pass
