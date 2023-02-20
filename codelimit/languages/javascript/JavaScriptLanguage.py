import os

from pygments.lexer import Lexer
from pygments.lexers import JavascriptLexer

from codelimit.common.Language import Language
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.utils import path_has_suffix
from codelimit.languages.javascript.JavaScriptScopeExtractor import JavaScriptScopeExtractor


class JavaScriptLanguage(Language):

    def accept_file(self, path: str) -> bool:
        parts = path.split(os.path.sep)
        if 'tests' in parts or 'node_modules' in parts:
            return False
        return path_has_suffix(path.lower(), 'js')

    def get_lexer(self) -> Lexer:
        return JavascriptLexer()

    def get_scope_extractor(self) -> ScopeExtractor:
        return JavaScriptScopeExtractor()
