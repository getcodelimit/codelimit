from codelimit.common.token_matching.predicate.And import And
from codelimit.common.token_matching.predicate.Keyword import Keyword
from codelimit.common.token_matching.predicate.Not import Not
from codelimit.common.token_matching.predicate.Symbol import Symbol
from tests.common.token_matching.predicates.utils import keyword_token, symbol_token


def test_and():
    predicate = And(Not(Symbol("{")), Not(Keyword("throws")))

    assert predicate.accept(symbol_token(";"))
    assert not predicate.accept(keyword_token("throws"))
    assert not predicate.accept(symbol_token("{"))
