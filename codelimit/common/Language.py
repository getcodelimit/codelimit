from abc import ABC, abstractmethod

from pygments.lexer import Lexer

from codelimit.common.ScopeExtractor import ScopeExtractor
from codelimit.common.Token import Token
from codelimit.common.source_utils import index_to_location, filter_tokens


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
        tokens = [Token(index_to_location(code, t[0]), t[1], t[2]) for t in lexer_tokens]

        def predicate(token: Token):
            if token.is_whitespace() or token.is_comment():
                return False
            return True

        return filter_tokens(tokens, predicate)
