import pytest
from pygments.lexers import PythonLexer
from pygments.lexers import CSharpLexer

from codelimit.common.gsm.matcher import find_all
from codelimit.common.gsm.operator.OneOrMore import OneOrMore
from codelimit.common.lexer_utils import lex
from codelimit.common.token_matching.predicate.Balanced import Balanced
from codelimit.common.token_matching.predicate.Keyword import Keyword
from codelimit.common.token_matching.predicate.Name import Name
from codelimit.common.token_matching.predicate.Symbol import Symbol
from codelimit.common.token_matching.predicate.TokenValue import TokenValue


def test_match_keyword():
    code = "def foo(): pass\ndef bar(): pass\n"
    tokens = lex(PythonLexer(), code)

    result = find_all(Keyword("def"), tokens)

    assert len(result) == 2
    assert result[0].token_string() == "def"
    assert result[1].token_string() == "def"


def test_match_name():
    code = "def foo(): pass\ndef bar(): pass\n"
    tokens = lex(PythonLexer(), code)

    result = find_all(Name(), tokens)

    assert len(result) == 2
    assert result[0].token_string() == "foo"
    assert result[1].token_string() == "bar"


def test_match_function_header():
    code = "def foo(): pass\ndef bar(): pass\n"
    tokens = lex(PythonLexer(), code)

    result = find_all([Keyword("def"), Name()], tokens)

    assert len(result) == 2
    assert result[0].token_string() == "def foo"
    assert result[1].token_string() == "def bar"


def test_reset_pattern():
    code = "foo bar()"
    tokens = lex(PythonLexer(), code)

    result = find_all([Name(), Balanced("(", ")")], tokens)

    assert len(result) == 1


def test_string_pattern():
    code = "def bar()"
    tokens = lex(PythonLexer(), code)

    result = find_all([TokenValue("def"), Name()], tokens)

    assert len(result) == 1


def test_ignore_incomplete_match():
    code = ""
    code += "def bar(\n"
    code += "def foo():\n"
    code += "  pass\n"
    tokens = lex(PythonLexer(), code)

    result = find_all([Keyword("def"), Name(), OneOrMore(Balanced("(", ")"))], tokens)

    assert len(result) == 1


@pytest.mark.skip
def test_predicate_follows_operator():
    code = "Split(new[] {' '})"
    tokens = lex(CSharpLexer(), code)

    result = find_all([Name(), OneOrMore(Balanced("(", ")")), Symbol('{')], tokens)

    assert len(result) == 1
