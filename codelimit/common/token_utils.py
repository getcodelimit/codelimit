from typing import Tuple

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange


def get_balanced_symbol_token_indices(
    tokens: list[Token], start: str, end: str, extract_nested=False
) -> list[Tuple[int, int]]:
    result = []
    block_starts = []
    for index, t in enumerate(tokens):
        if t.is_symbol(start):
            block_starts.append(index)
        elif t.is_symbol(end):
            if len(block_starts) > 0:
                start_index = block_starts.pop()
                if extract_nested or len(block_starts) == 0:
                    result.append((start_index, index))
    return result


def get_balanced_symbol_token_ranges(
    tokens: list[Token], start: str, end: str
) -> list[TokenRange]:
    result = []
    token_lists = []
    for index, t in enumerate(tokens):
        if t.is_symbol(start):
            token_lists.append([t])
        elif t.is_symbol(end):
            if len(token_lists) > 0:
                token_lists[-1].append(t)
                tokens = token_lists.pop()
                result.append(TokenRange(tokens))
        else:
            if len(token_lists) > 0:
                token_lists[-1].append(t)
    return result


def sort_tokens(tokens: list[Token]) -> list[Token]:
    result = sorted(tokens, key=lambda t: t.location.column)
    result = sorted(result, key=lambda t: t.location.line)
    return result


def sort_token_ranges(token_ranges: list[TokenRange]) -> list[TokenRange]:
    return sorted(
        token_ranges,
        key=lambda tr: (tr.tokens[0].location.line, tr.tokens[0].location.column),
    )
