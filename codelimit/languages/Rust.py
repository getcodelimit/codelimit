from codelimit.common.Language import Language
from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.gsm.operator.ZeroOrMore import ZeroOrMore
from codelimit.common.scope.Header import Header
from codelimit.common.scope.scope_utils import (
    get_blocks,
    get_headers,
)
from codelimit.common.token_matching.predicate.And import And
from codelimit.common.token_matching.predicate.Keyword import Keyword
from codelimit.common.token_matching.predicate.Name import Name
from codelimit.common.token_matching.predicate.Not import Not
from codelimit.common.token_matching.predicate.Symbol import Symbol


class Rust(Language):
    def __init__(self):
        super().__init__("Rust")

    def extract_headers(self, tokens: list[Token]) -> list[Header]:
        return get_headers(
            tokens,
            [Keyword("fn"), Name()],
            [ZeroOrMore(And(Not(";"), Not("{"))), Symbol("{")],
            nested=True,
        )

    def extract_blocks(
        self, tokens: list[Token], headers: list[Header]
    ) -> list[TokenRange]:
        return get_blocks(tokens, "{", "}")
