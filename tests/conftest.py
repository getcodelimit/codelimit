from textwrap import dedent

from pygments.lexers import get_lexer_by_name

from codelimit.common.Language import Language
from codelimit.common.lexer_utils import lex
from codelimit.common.scope.scope_utils import build_scopes, unfold_scopes, count_lines
from codelimit.common.source_utils import filter_tokens


def assert_functions(code: str, language: Language, functions: dict[str, int]):
    code = dedent(code).strip("\n")
    lexer = get_lexer_by_name(language.name)
    tokens = lex(lexer, code, False)
    code_tokens = filter_tokens(tokens)
    scopes = build_scopes(tokens, language)
    scopes = unfold_scopes(scopes)
    assert len(scopes) == len(functions)
    for idx, scope in enumerate(scopes):
        assert scope.header.name() in functions
        assert count_lines(scope, code_tokens) == functions[scope.header.name()]


def print_scopes(code: str, language: Language):
    code = dedent(code).strip("\n")
    lexer = get_lexer_by_name(language.name)
    tokens = lex(lexer, code, False)
    code_tokens = filter_tokens(tokens)
    scopes = build_scopes(tokens, language)
    scopes = unfold_scopes(scopes)
    print()
    for scope in scopes:
        print(f"{scope.header.name()}: {count_lines(scope, code_tokens)}")
