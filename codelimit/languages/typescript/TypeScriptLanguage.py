from typing import Union

from pygments.lexer import Lexer
from pygments.lexers import TypeScriptLexer

from codelimit.common.Language import Language
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.languages.typescript.TypeScriptScopeExtractor import (
    TypeScriptScopeExtractor,
)


class TypeScriptLanguage(Language):
    def get_file_extension(self) -> Union[str, list[str]]:
        return "ts"

    def get_lexer(self) -> Lexer:
        return TypeScriptLexer()

    def get_scope_extractor(self) -> ScopeExtractor:
        return TypeScriptScopeExtractor()
