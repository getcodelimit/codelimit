from pygments.token import Punctuation

from codelimit.common.Location import Location
from codelimit.common.Token import Token
from codelimit.common.token_matching.BalancedPredicate import BalancedPredicate
from codelimit.common.token_matching.TokenMatching import SymbolPredicate


def test_simple():
    predicate = BalancedPredicate(SymbolPredicate("("), SymbolPredicate(")"))

    assert not predicate.accept(Token(Location(1, 1), Punctuation, "["))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "("))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "["))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "]"))
    assert predicate.accept(Token(Location(1, 1), Punctuation, ")"))
    assert not predicate.accept(Token(Location(1, 1), Punctuation, "]"))


def test_nested():
    predicate = BalancedPredicate(SymbolPredicate("("), SymbolPredicate(")"))

    assert predicate.accept(Token(Location(1, 1), Punctuation, "("))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "("))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "["))
    assert predicate.accept(Token(Location(1, 1), Punctuation, "]"))
    assert predicate.accept(Token(Location(1, 1), Punctuation, ")"))
    assert predicate.accept(Token(Location(1, 1), Punctuation, ")"))
    assert not predicate.accept(Token(Location(1, 1), Punctuation, "["))


def test_unbalanced():
    predicate = BalancedPredicate(SymbolPredicate("("), SymbolPredicate(")"))

    assert predicate.accept(Token(Location(1, 1), Punctuation, "("))
    assert predicate.accept(Token(Location(1, 1), Punctuation, ")"))
    assert not predicate.accept(Token(Location(1, 1), Punctuation, ")"))
