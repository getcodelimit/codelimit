from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.scope.scope_extractor_utils import (
    has_name_prefix,
    has_curly_suffix,
)
from codelimit.common.token_utils import get_balanced_symbol_token_indices


class CScopeExtractor(ScopeExtractor):
    def extract_headers(self, tokens: list[Token]) -> list[Header]:
        result = []
        balanced_tokens = get_balanced_symbol_token_indices(tokens, "(", ")")
        for bt in balanced_tokens:
            if has_name_prefix(tokens, bt[0]) and has_curly_suffix(tokens, bt[1]):
                result.append(
                    Header(
                        tokens[bt[0] - 1].value,
                        TokenRange(tokens[bt[0] - 1 : bt[1] + 1]),
                    )
                )
        return result

    def extract_blocks(
        self, tokens: list[Token], headers: list[Header]
    ) -> list[TokenRange]:
        balanced_tokens = get_balanced_symbol_token_indices(tokens, "{", "}", False)
        blocks = [TokenRange(tokens[bt[0] : bt[1] + 1]) for bt in balanced_tokens]
        sorted_by_line = sorted(blocks, key=lambda tr: tr.tokens[0].location.line)
        sorted_by_columns = sorted(
            sorted_by_line, key=lambda tr: tr.tokens[0].location.column
        )
        return sorted_by_columns
