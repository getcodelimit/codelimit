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
    start_indices: list[int] = []
    for index, t in enumerate(tokens):
        if t.is_symbol(start):
            start_indices.append(index)
        elif t.is_symbol(end):
            if len(start_indices) > 0:
                start_index = start_indices.pop()
                result.append(TokenRange(start_index, index + 1))
    return result


def sort_tokens(tokens: list[Token]) -> list[Token]:
    result = sorted(tokens, key=lambda t: t.location.column)
    result = sorted(result, key=lambda t: t.location.line)
    return result
