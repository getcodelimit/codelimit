from typing import Tuple

from codelimit.common.Token import Token


def get_balanced_symbol_token_indices(
    tokens: list[Token], start: str, end: str, nested=False
) -> list[Tuple[int, int]]:
    result = []
    block_starts = []
    for index, t in enumerate(tokens):
        if t.is_symbol(start):
            block_starts.append(index)
        elif t.is_symbol(end):
            if len(block_starts) > 0:
                start_index = block_starts.pop()
                if nested or len(block_starts) == 0:
                    result.append((start_index, index))
    return result


def sort_tokens(tokens: list[Token]) -> list[Token]:
    result = sorted(tokens, key=lambda t: t.location.column)
    result = sorted(result, key=lambda t: t.location.line)
    return result
