import os
from abc import ABC, abstractmethod
from typing import Union

from pygments.lexer import Lexer

from codelimit.common.Location import Location
from codelimit.common.Token import Token
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.source_utils import filter_tokens, get_newline_indices
from codelimit.common.utils import path_has_extension, get_basename


class Language(ABC):
    def accept_file(self, path: str) -> bool:
        ignore_folders = ["tests", "node_modules", "venv"]
        parts = path.split(os.path.sep)
        for part in parts:
            if part in ignore_folders:
                return False
        if get_basename(path).startswith("test"):
            return False
        return path_has_extension(path.lower(), self.get_file_extension())

    @abstractmethod
    def get_file_extension(self) -> Union[str, list[str]]:
        pass

    @abstractmethod
    def get_lexer(self) -> Lexer:
        pass

    @abstractmethod
    def get_scope_extractor(self) -> ScopeExtractor:
        pass

    def lex(self, code: str) -> list[Token]:
        lexer = self.get_lexer()
        lexer_tokens = lexer.get_tokens_unprocessed(code)
        indices = get_newline_indices(code)
        if len(indices) == 0:
            tokens = [Token(Location(1, t[0] + 1), t[1], t[2]) for t in lexer_tokens]
        else:
            tokens = []
            newline_index = 0
            line_start = 0
            for t in lexer_tokens:
                while newline_index < len(indices) and t[0] > indices[newline_index]:
                    line_start = indices[newline_index] + 1
                    newline_index += 1
                tokens.append(
                    Token(
                        Location(newline_index + 1, t[0] - line_start + 1), t[1], t[2]
                    )
                )

        def predicate(token: Token):
            if token.is_whitespace() or token.is_comment():
                return False
            return True

        return filter_tokens(tokens, predicate)
