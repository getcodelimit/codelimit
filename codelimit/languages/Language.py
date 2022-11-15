from abc import ABC, abstractmethod

from codelimit.common.Token import Token
from codelimit.languages.ScopeExtractor import ScopeExtractor


class Language(ABC):
    @abstractmethod
    def accept_file(self, path: str) -> bool:
        pass

    @abstractmethod
    def lex(self, code: str) -> list[Token]:
        pass

    @abstractmethod
    def get_scope_extractor(self) -> ScopeExtractor:
        pass

