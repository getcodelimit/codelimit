from __future__ import annotations

from abc import ABC, abstractmethod

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header


class Language(ABC):

    def __init__(self, name: str, allow_nested_functions=True):
        self.name = name
        self.allow_nested_functions = allow_nested_functions

    @abstractmethod
    def extract_headers(self, tokens: list[Token]) -> list[Header]:
        pass

    @abstractmethod
    def extract_blocks(
            self, tokens: list[Token], headers: list[Header]
    ) -> list[TokenRange]:
        pass
