from abc import ABC, abstractmethod

from pygments.lexer import Lexer

from codelimit.common.ScopeExtractor import ScopeExtractor
from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.Token import Token
from codelimit.common.source_utils import filter_tokens, get_newline_indices


class Language(ABC):
    @abstractmethod
    def accept_file(self, path: str) -> bool:
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
            tokens = [Token(SourceLocation(1, t[0] + 1), t[1], t[2]) for t in lexer_tokens]
        else:
            tokens = []
            newline_index = 0
            line_start = 0
            for t in lexer_tokens:
                while t[0] > indices[newline_index] and newline_index < len(indices) - 1:
                    line_start = indices[newline_index] + 1
                    newline_index += 1
                tokens.append(Token(SourceLocation(newline_index + 1, t[0] - line_start + 1), t[1], t[2]))

        def predicate(token: Token):
            if token.is_whitespace() or token.is_comment():
                return False
            return True

        return filter_tokens(tokens, predicate)
