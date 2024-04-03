from pygments.token import Punctuation

from codelimit.common.Location import Location
from codelimit.common.Token import Token
from codelimit.common.token_matching.predicate.Balanced import Balanced
from codelimit.common.token_matching.predicate.Symbol import Symbol


def test_simple():
    predicate = Balanced(Symbol("("), Symbol(")"))

    assert not predicate.accept(Token(Location(1, 1), Punctuation, "["))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "("))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "["))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "]"))
    assert predicate.accept(Token(Location(1, 1), Punctuation, ")"))
    assert not predicate.accept(Token(Location(1, 1), Punctuation, "]"))


def test_construct_with_string():
    predicate = Balanced("(", ")")

    assert predicate.accept(Token(Location(1, 1), Punctuation, "("))
    assert predicate.accept(Token(Location(1, 1), Punctuation, ")"))


def test_nested():
    predicate = Balanced(Symbol("("), Symbol(")"))

    assert predicate.accept(Token(Location(1, 1), Punctuation, "("))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "("))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "["))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "]"))
    assert predicate.accept(Token(Location(1, 1), Punctuation, ")"))
    assert predicate.accept(Token(Location(1, 1), Punctuation, ")"))
    assert not predicate.accept(Token(Location(1, 1), Punctuation, "["))


def test_unbalanced():
    predicate = Balanced(Symbol("("), Symbol(")"))

    assert predicate.accept(Token(Location(1, 1), Punctuation, "("))
    assert predicate.accept(Token(Location(1, 1), Punctuation, ")"))
    assert not predicate.accept(Token(Location(1, 1), Punctuation, ")"))
