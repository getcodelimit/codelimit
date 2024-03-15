from textwrap import dedent

from pygments.lexers import get_lexer_by_name

from codelimit.common.lexer_utils import lex
from codelimit.common.scope.scope_utils import build_scopes
from codelimit.common.utils import load_language_by_name
from codelimit.languages import LanguageName


def assert_units(code: str, language_name: LanguageName, units: dict[str, int]):
    code = dedent(code).strip('\n')
    lexer = get_lexer_by_name(language_name.value)
    tokens = lex(lexer, code, False)
    language = load_language_by_name(language_name.value)
    if not language:
        raise ValueError(f"Language not found: {language_name.value}")
    scopes = build_scopes(tokens, language)
    assert len(scopes) == len(units)
    for idx, scope in enumerate(scopes):
        assert scope.header.name in units
        assert len(scope) == units[scope.header.name]
