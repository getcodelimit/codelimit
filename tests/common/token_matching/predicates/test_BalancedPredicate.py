from codelimit.common.token_matching.predicate.Balanced import Balanced
from codelimit.common.token_matching.predicate.Symbol import Symbol
from tests.common.token_matching.predicates.utils import symbol_token


def test_simple():
    predicate = Balanced(Symbol("("), Symbol(")"))

    assert not predicate.accept(symbol_token("["))
    assert predicate.accept(symbol_token("("))
    assert predicate.accept(symbol_token("["))
    assert predicate.accept(symbol_token("]"))
    assert predicate.accept(symbol_token(")"))
    assert not predicate.accept(symbol_token("]"))


def test_construct_with_string():
    predicate = Balanced("(", ")")

    assert predicate.accept(symbol_token("("))
    assert predicate.accept(symbol_token(")"))


def test_nested():
    predicate = Balanced(Symbol("("), Symbol(")"))

    assert predicate.accept(symbol_token("("))
    assert predicate.accept(symbol_token("("))
    assert predicate.accept(symbol_token("["))
    assert predicate.accept(symbol_token("]"))
    assert predicate.accept(symbol_token(")"))
    assert predicate.accept(symbol_token(")"))
    assert not predicate.accept(symbol_token("["))


def test_unbalanced():
    predicate = Balanced(Symbol("("), Symbol(")"))

    assert predicate.accept(symbol_token("("))
    assert predicate.accept(symbol_token(")"))
    assert not predicate.accept(symbol_token(")"))
