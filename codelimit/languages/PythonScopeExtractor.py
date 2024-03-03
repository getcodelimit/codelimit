from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.token_matching.BalancedPredicate import BalancedPredicate
from codelimit.common.token_matching.TokenMatching import (
    match,
    KeywordPredicate,
    NamePredicate,
    SymbolPredicate,
)
from codelimit.common.utils import delete_indices


class PythonScopeExtractor(ScopeExtractor):
    def extract_headers(self, tokens: list[Token]) -> list[Header]:
        result = []
        matches = match(
            tokens,
            [
                KeywordPredicate("def"),
                NamePredicate(),
                BalancedPredicate(SymbolPredicate("("), SymbolPredicate(")")),
            ],
        )
        for m in matches:
            result.append(Header(m.tokens[1].value, m))
        return result

    def extract_blocks(
        self, tokens: list[Token], headers: list[Header]
    ) -> list[TokenRange]:
        lines = _get_token_lines(tokens)
        result = []
        reverse_headers = headers[::-1]
        for header in reverse_headers:
            header_line_nr = header.token_range.tokens[-1].location.line
            header_indentation = header.token_range.tokens[0].location.column
            block_line_indices = []
            for idx, line in enumerate(lines[::-1]):
                line_index = (len(lines) - 1) - idx
                line_nr = line[0].location.line
                line_indentation = line[0].location.column
                if line_nr <= header_line_nr:
                    break
                elif line_indentation > header_indentation:
                    block_line_indices.append(line_index)
                else:
                    block_line_indices = []
            if len(block_line_indices) > 0:
                scope_tokens = []
                for index in block_line_indices[::-1]:
                    scope_tokens.extend(lines[index])
                result.append(TokenRange(scope_tokens))
                lines = delete_indices(lines, block_line_indices)
        return result[::-1]


def _get_token_lines(tokens: list[Token]) -> list[list[Token]]:
    result = []
    line: list[Token] = []
    line_continuation = False
    line_nr = 0
    for t in tokens:
        if len(line) == 0:
            line.append(t)
            line_nr = t.location.line
        else:
            if line_continuation:
                line.append(t)
                line_nr = t.location.line
                line_continuation = False
            if t.location.line == line_nr:
                line.append(t)
                if t.value.endswith("\\\n"):
                    line_continuation = True
            else:
                result.append(line)
                line = [t]
                line_nr = t.location.line
    if len(line) > 0:
        result.append(line)
    return result


def _get_indentation(line: str):
    result = 0
    for c in line:
        if c == " ":
            result += 1
        elif c == "\t":
            result += 4
        else:
            return result
    return None
