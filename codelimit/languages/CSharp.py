from codelimit.common.Language import Language
from codelimit.common.gsm.operator.OneOrMore import OneOrMore
from codelimit.common.scope.scope_utils import (
    get_blocks,
    get_headers,
)
from codelimit.common.token_matching.predicate.Balanced import Balanced
from codelimit.common.token_matching.predicate.Name import Name
from codelimit.common.token_matching.predicate.Symbol import Symbol


class CSharp(Language):
    def __init__(self):
        super().__init__('C#')

    def extract_headers(self, tokens: list) -> list:
        return get_headers(tokens, [Name(), OneOrMore(Balanced('(', ')'))], Symbol('{'))

    def extract_blocks(self, tokens: list, headers: list) -> list:
        return get_blocks(tokens, "{", "}")
