from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.token_utils import get_balanced_symbol_token_indices


class TypeScriptScopeExtractor(ScopeExtractor):
    def extract_headers(self, tokens: list[Token]) -> list[Header]:
        result = []
        balanced_tokens = get_balanced_symbol_token_indices(tokens, "(", ")")

        def has_name_prefix(index):
            return index > 0 and tokens[index - 1].is_name()

        def has_curly_suffix(index):
            return index < len(tokens) - 1 and tokens[index + 1].is_symbol("{")

        for bt in balanced_tokens:
            if has_name_prefix(bt[0]) and has_curly_suffix(bt[1]):
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
