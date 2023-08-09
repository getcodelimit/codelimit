from typing import Union

from pygments.lexer import Lexer
from pygments.lexers import CLexer

from codelimit.common.Language import Language
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.languages.c.CScopeExtractor import CScopeExtractor


class CLanguage(Language):
    def get_file_extension(self) -> Union[str, list[str]]:
        return ["c", "h"]

    def get_lexer(self) -> Lexer:
        return CLexer()

    def get_scope_extractor(self) -> ScopeExtractor:
        return CScopeExtractor()
