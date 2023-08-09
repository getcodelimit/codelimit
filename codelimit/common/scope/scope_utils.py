from typing import Optional

from codelimit.common.Language import Language
from codelimit.common.scope.Header import Header
from codelimit.common.scope.Scope import Scope
from codelimit.common.TokenRange import TokenRange
from codelimit.common.token_utils import sort_tokens
from codelimit.common.utils import delete_indices


def build_scopes(language: Language, code: str) -> list[Scope]:
    tokens = language.lex(code)
    scope_extractor = language.get_scope_extractor()
    headers = scope_extractor.extract_headers(tokens)
    blocks = scope_extractor.extract_blocks(tokens, headers)
    return _build_scopes_from_headers_and_blocks(headers, blocks)


def _build_scopes_from_headers_and_blocks(
    headers: list[Header], blocks: list[TokenRange]
) -> list[Scope]:
    result: list[Scope] = []
    reverse_headers = headers[::-1]
    for header in reverse_headers:
        scope_blocks_indices = _find_scope_blocks_indices(header.token_range, blocks)
        if len(scope_blocks_indices) > 0:
            scope_tokens = []
            for i in scope_blocks_indices:
                scope_tokens.extend(blocks[i].tokens)
            scope_tokens = sort_tokens(scope_tokens)
            scope_block = TokenRange(scope_tokens)
            result.append(Scope(header, scope_block))
            blocks = delete_indices(blocks, scope_blocks_indices)
    result.reverse()
    return result


def _find_scope_blocks_indices(
    header: TokenRange, blocks: list[TokenRange]
) -> list[int]:
    body_block = _get_closest_block(header, blocks)
    if body_block:
        if body_block.contains(header):
            return [i for i in range(len(blocks)) if body_block.contains(blocks[i])]
        else:
            return [i for i in range(len(blocks)) if body_block.overlaps(blocks[i])]
    return []


def _get_closest_block(
    header: TokenRange, blocks: list[TokenRange]
) -> Optional[TokenRange]:
    for block in blocks:
        if block.contains(header):
            return block
        if block.gt(header):
            return block
    return None
