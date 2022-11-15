from pygments.lexers import PythonLexer

from codelimit.common.Token import Token
from codelimit.languages.Language import Language
from codelimit.languages.ScopeExtractor import ScopeExtractor
from codelimit.languages.python.PythonScopeExtractor import PythonScopeExtractor


class PythonLanguage(Language):

    def accept_file(self, path: str) -> bool:
        return path.lower().endswith('.py')

    def lex(self, code: str) -> list[Token]:
        return [Token(t[0], t[1], t[2]) for t in PythonLexer().get_tokens_unprocessed(code)]

    def get_scope_extractor(self) -> ScopeExtractor:
        return PythonScopeExtractor()
