from abc import ABC, abstractmethod

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header


class ScopeExtractor(ABC):
    def __init__(self, allow_nested_scopes=False):
        self.allow_nested_scopes = allow_nested_scopes

    @abstractmethod
    def extract_headers(self, tokens: list[Token]) -> list[Header]:
        pass

    @abstractmethod
    def extract_blocks(
        self, tokens: list[Token], headers: list[Header]
    ) -> list[TokenRange]:
        pass
