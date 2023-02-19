import os.path

from pygments.lexer import Lexer
from pygments.lexers import PythonLexer

from codelimit.common.Language import Language
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.utils import path_has_suffix, get_basename
from codelimit.languages.python.PythonScopeExtractor import PythonScopeExtractor


class PythonLanguage(Language):

    def accept_file(self, path: str) -> bool:
        parts = path.split(os.path.sep)
        if 'tests' in parts or 'venv' in parts:
            return False
        if get_basename(path).startswith('test'):
            return False
        return path_has_suffix(path.lower(), 'py')

    def get_lexer(self) -> Lexer:
        return PythonLexer()

    def get_scope_extractor(self) -> ScopeExtractor:
        return PythonScopeExtractor()
