from codelimit.common.ScopeExtractor import ScopeExtractor
from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.token_utils import get_balanced_symbol_token_indices


class CScopeExtractor(ScopeExtractor):
    def extract_headers(self, tokens: list[Token]) -> list[TokenRange]:
        result = []
        balanced_tokens = get_balanced_symbol_token_indices(tokens, '(', ')')

        def has_name_prefix(index):
            return index > 0 and tokens[index - 1].is_name()

        def has_curly_suffix(index):
            return index < len(tokens) - 1 and tokens[index + 1].is_symbol('{')

        for bt in balanced_tokens:
            if has_name_prefix(bt[0]) and has_curly_suffix(bt[1]):
                result.append(TokenRange(tokens[bt[0] - 1:bt[1] + 1]))
        return result

    def extract_blocks(self, tokens: list[Token]) -> list[TokenRange]:
        balanced_tokens = get_balanced_symbol_token_indices(tokens, '{', '}', True)
        return [TokenRange(tokens[bt[0]:bt[1] + 1]) for bt in balanced_tokens]
