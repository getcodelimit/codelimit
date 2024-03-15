from codelimit.common.Language import Language
from codelimit.common.scope.scope_utils import (
    get_blocks,
    get_headers,
)
from codelimit.common.token_matching.predicates.Balanced import Balanced
from codelimit.common.token_matching.predicates.Lookahead import Lookahead
from codelimit.common.token_matching.predicates.Name import Name
from codelimit.common.token_matching.predicates.Symbol import Symbol


class Java(Language):
    def __init__(self):
        super().__init__(True)

    def extract_headers(self, tokens: list) -> list:
        return get_headers(tokens, [Name(), Balanced("(", ")"), Lookahead(Symbol("{"))])

        # result = []
        # balanced_tokens = get_balanced_symbol_token_indices(tokens, "(", ")")
        # for bt in balanced_tokens:
        #     if has_name_prefix(tokens, bt[0]) and has_curly_suffix(tokens, bt[1]):
        #         result.append(
        #             Header(
        #                 tokens[bt[0] - 1].value,
        #                 TokenRange(tokens[bt[0] - 1 : bt[1] + 1]),
        #             )
        #         )
        # return result

    def extract_blocks(self, tokens: list, headers: list) -> list:
        return get_blocks(tokens, "{", "}", True)
