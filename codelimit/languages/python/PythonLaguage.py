from pygments.lexer import Lexer
from pygments.lexers import PythonLexer

from codelimit.common.Language import Language
from codelimit.common.ScopeExtractor import ScopeExtractor
from codelimit.languages.python.PythonScopeExtractor import PythonScopeExtractor


class PythonLanguage(Language):

    def accept_file(self, path: str) -> bool:
        return path.lower().endswith('.py')

    def get_lexer(self) -> Lexer:
        return PythonLexer()

    def get_scope_extractor(self) -> ScopeExtractor:
        return PythonScopeExtractor()
