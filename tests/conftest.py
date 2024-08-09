from textwrap import dedent

from pygments.lexers import get_lexer_by_name

from codelimit.common.Language import Language
from codelimit.common.lexer_utils import lex
from codelimit.common.scope.Scope import Scope
from codelimit.common.scope.scope_utils import build_scopes, unfold_scopes


def extract_units(code: str, language: Language) -> list[Scope]:
    code = dedent(code).strip("\n")
    lexer = get_lexer_by_name(language.name)
    tokens = lex(lexer, code, False)
    return build_scopes(tokens, language)


def assert_units(code: str, language: Language, units: dict[str, int]):
    scopes = extract_units(code, language)
    scopes = unfold_scopes(scopes)
    assert len(scopes) == len(units)
    for idx, scope in enumerate(scopes):
        assert scope.header.name in units
        assert len(scope) == units[scope.header.name]


def print_units(code: str, language: Language):
    scopes = extract_units(code, language)
    scopes = unfold_scopes(scopes)
    print()
    for scope in scopes:
        print(f"{scope.header.name}: {len(scope)}")
