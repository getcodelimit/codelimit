from codelimit.common.token_matching.predicate.Not import Not
from codelimit.common.token_matching.predicate.Symbol import Symbol
from tests.common.token_matching.predicates.utils import symbol_token, keyword_token, operator_token


def test_not():
    predicate = Not(Symbol("{"))

    assert not predicate.accept(symbol_token("{"))
    assert predicate.accept(keyword_token("throws"))
    assert predicate.accept(operator_token("+"))


def test_not_not():
    predicate = Not(Not(Symbol("{")))

    assert predicate.accept(symbol_token("{"))
    assert not predicate.accept(keyword_token("throws"))
    assert not predicate.accept(operator_token("+"))
