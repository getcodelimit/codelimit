from pygments.lexers import PythonLexer

from codelimit.common.lexer_utils import lex
from codelimit.common.token_matching.TokenMatcher import TokenMatcher
from codelimit.common.token_matching.predicate.Balanced import Balanced
from codelimit.common.token_matching.predicate.Keyword import Keyword
from codelimit.common.token_matching.predicate.Name import Name


def test_match_keyword():
    code = "def foo(): pass\ndef bar(): pass\n"
    tokens = lex(PythonLexer(), code)

    result = TokenMatcher(Keyword("def")).match(tokens)

    assert len(result) == 2
    assert result[0].token_string() == "def"
    assert result[1].token_string() == "def"


def test_match_name():
    code = "def foo(): pass\ndef bar(): pass\n"
    tokens = lex(PythonLexer(), code)

    result = TokenMatcher(Name()).match(tokens)

    assert len(result) == 2
    assert result[0].token_string() == "foo"
    assert result[1].token_string() == "bar"


def test_match_function_header():
    code = "def foo(): pass\ndef bar(): pass\n"
    tokens = lex(PythonLexer(), code)

    result = TokenMatcher([Keyword("def"), Name()]).match(tokens)

    assert len(result) == 2
    assert result[0].token_string() == "def foo"
    assert result[1].token_string() == "def bar"


def test_reset_pattern():
    code = "foo bar()"
    tokens = lex(PythonLexer(), code)

    result = TokenMatcher([Name(), Balanced("(", ")")]).match(tokens)

    assert len(result) == 1


def test_string_pattern():
    code = "def bar()"
    tokens = lex(PythonLexer(), code)

    result = TokenMatcher(["def", Name()]).match(tokens)

    assert len(result) == 1


def test_ignore_incomplete_match():
    code = ""
    code += "def bar(\n"
    code += "def foo():\n"
    code += "  pass\n"
    tokens = lex(PythonLexer(), code)

    result = TokenMatcher(["def", Name(), Balanced("(", ")")]).match(tokens)

    assert len(result) == 1
