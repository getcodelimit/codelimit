from typing import Union

from pygments.lexer import Lexer
from pygments.lexers import JavascriptLexer

from codelimit.common.Language import Language
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.languages.javascript.JavaScriptScopeExtractor import (
    JavaScriptScopeExtractor,
)


class JavaScriptLanguage(Language):
    def get_file_extension(self) -> Union[str, list[str]]:
        return "js"

    def get_lexer(self) -> Lexer:
        return JavascriptLexer()

    def get_scope_extractor(self) -> ScopeExtractor:
        return JavaScriptScopeExtractor()
