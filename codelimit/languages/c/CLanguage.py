from pygments.lexer import Lexer
from pygments.lexers import CLexer

from codelimit.common.Language import Language
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.utils import path_has_suffix
from codelimit.languages.c.CScopeExtractor import CScopeExtractor


class CLanguage(Language):

    def accept_file(self, path: str) -> bool:
        return path_has_suffix(path.lower(), ["c", 'h'])

    def get_lexer(self) -> Lexer:
        return CLexer()

    def get_scope_extractor(self) -> ScopeExtractor:
        return CScopeExtractor()
