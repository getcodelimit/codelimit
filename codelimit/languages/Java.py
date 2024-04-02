from codelimit.common.Language import Language
from codelimit.common.scope.scope_utils import (
    get_blocks,
    get_headers,
)
from codelimit.common.token_matching.predicates.Balanced import Balanced
from codelimit.common.token_matching.predicates.Lookahead import Lookahead
from codelimit.common.token_matching.predicates.Name import Name
from codelimit.common.token_matching.predicates.Or import Or


class Java(Language):
    def extract_headers(self, tokens: list) -> list:
        return get_headers(
            tokens, [Name(), Balanced("(", ")"), Lookahead(Or("{", "throws"))]
        )

    def extract_blocks(self, tokens: list, headers: list) -> list:
        return get_blocks(tokens, "{", "}")
