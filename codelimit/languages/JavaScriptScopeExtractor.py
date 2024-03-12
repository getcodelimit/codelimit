from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.scope.scope_extractor_utils import get_balanced_blocks, has_name_prefix, has_curly_suffix
from codelimit.common.token_utils import get_balanced_symbol_token_indices


class JavaScriptScopeExtractor(ScopeExtractor):
    def extract_headers(self, tokens: list[Token]) -> list[Header]:
        result = []
        balanced_tokens = get_balanced_symbol_token_indices(tokens, "(", ")")
        for bt in balanced_tokens:
            if has_name_prefix(tokens, bt[0]) and has_curly_suffix(tokens, bt[1]):
                result.append(
                    Header(
                        tokens[bt[0] - 1].value,
                        TokenRange(tokens[bt[0] - 1: bt[1] + 1]),
                    )
                )
        return result

    def extract_blocks(
            self, tokens: list[Token], headers: list[Header]
    ) -> list[TokenRange]:
        return get_balanced_blocks(tokens, "{", "}")
