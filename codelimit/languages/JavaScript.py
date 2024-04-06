from codelimit.common.Language import Language
from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.gsm.operator.OneOrMore import OneOrMore
from codelimit.common.gsm.operator.Optional import Optional
from codelimit.common.scope.Header import Header
from codelimit.common.scope.scope_utils import (
    get_blocks,
    get_headers,
)
from codelimit.common.token_matching.predicate.Balanced import Balanced
from codelimit.common.token_matching.predicate.Keyword import Keyword
from codelimit.common.token_matching.predicate.Name import Name
from codelimit.common.token_matching.predicate.Symbol import Symbol


class JavaScript(Language):
    def extract_headers(self, tokens: list[Token]) -> list[Header]:
        return get_headers(
            tokens,
            [Optional(Keyword("function")), Name(), OneOrMore(Balanced("(", ")"))],
            Symbol("{"),
        )

    def extract_blocks(
        self, tokens: list[Token], headers: list[Header]
    ) -> list[TokenRange]:
        return get_blocks(tokens, "{", "}")
