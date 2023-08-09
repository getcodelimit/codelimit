from typing import Union

from pygments.lexer import Lexer
from pygments.lexers import PythonLexer

from codelimit.common.Language import Language
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.languages.python.PythonScopeExtractor import PythonScopeExtractor


class PythonLanguage(Language):
    def get_file_extension(self) -> Union[str, list[str]]:
        return "py"

    def get_lexer(self) -> Lexer:
        return PythonLexer()

    def get_scope_extractor(self) -> ScopeExtractor:
        return PythonScopeExtractor()
