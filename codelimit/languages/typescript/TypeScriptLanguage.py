import os

from pygments.lexer import Lexer
from pygments.lexers import TypeScriptLexer

from codelimit.common.Language import Language
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.utils import path_has_suffix
from codelimit.languages.typescript.TypeScriptScopeExtractor import TypeScriptScopeExtractor


class TypeScriptLanguage(Language):

    def accept_file(self, path: str) -> bool:
        parts = path.split(os.path.sep)
        if 'tests' in parts or 'node_modules' in parts:
            return False
        return path_has_suffix(path.lower(), 'ts')

    def get_lexer(self) -> Lexer:
        return TypeScriptLexer()

    def get_scope_extractor(self) -> ScopeExtractor:
        return TypeScriptScopeExtractor()
