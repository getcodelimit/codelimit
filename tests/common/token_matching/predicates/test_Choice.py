from codelimit.common.token_matching.predicate.Choice import Choice
from codelimit.common.token_matching.predicate.Keyword import Keyword
from codelimit.common.token_matching.predicate.Symbol import Symbol
from tests.common.token_matching.predicates.utils import keyword_token, symbol_token, operator_token


def test_choice():
    predicate = Choice(Symbol("{"), Keyword("throws"))

    assert predicate.accept(symbol_token("{"))
    assert predicate.accept(keyword_token("throws"))
    assert not predicate.accept(operator_token("+"))
