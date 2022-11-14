from abc import ABC, abstractmethod

from codelimit.languages.ScopeExtractor import ScopeExtractor


class Language(ABC):
    @abstractmethod
    def accept_file(self, path: str) -> bool:
        pass

    @abstractmethod
    def get_scope_extractor(self) -> ScopeExtractor:
        pass
