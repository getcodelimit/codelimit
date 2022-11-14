from abc import ABC, abstractmethod

from codelimit.common.SourceRange import SourceRange


class ScopeExtractor(ABC):
    @abstractmethod
    def extract_blocks(self, code: str) -> list[SourceRange]:
        pass

    @abstractmethod
    def extract_headers(self, code: str) -> list[SourceRange]:
        pass
