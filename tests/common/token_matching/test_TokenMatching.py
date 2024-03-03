from pygments.lexers import PythonLexer

from codelimit.common.lexer_utils import lex
from codelimit.common.token_matching.TokenMatching import (
    match,
    KeywordPredicate,
    NamePredicate,
)


def test_match_keyword():
    code = "def foo(): pass\ndef bar(): pass\n"
    tokens = lex(PythonLexer(), code)

    result = match(tokens, KeywordPredicate("def"))

    assert len(result) == 2
    assert result[0].token_string() == "def"
    assert result[1].token_string() == "def"


def test_match_name():
    code = "def foo(): pass\ndef bar(): pass\n"
    tokens = lex(PythonLexer(), code)

    result = match(tokens, NamePredicate())

    assert len(result) == 2
    assert result[0].token_string() == "foo"
    assert result[1].token_string() == "bar"


def test_match_function_header():
    code = "def foo(): pass\ndef bar(): pass\n"
    tokens = lex(PythonLexer(), code)

    result = match(tokens, [KeywordPredicate("def"), NamePredicate()])

    assert len(result) == 2
    assert result[0].token_string() == "def foo"
    assert result[1].token_string() == "def bar"
