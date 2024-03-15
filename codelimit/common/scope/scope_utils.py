from typing import Optional

from codelimit.common.Language import Language
from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header
from codelimit.common.scope.Scope import Scope
from codelimit.common.source_utils import filter_tokens, filter_nocl_comment_tokens
from codelimit.common.token_matching.TokenMatching import match, TokenPredicate
from codelimit.common.token_utils import sort_tokens, get_balanced_symbol_token_indices
from codelimit.common.utils import delete_indices


def build_scopes(tokens: list[Token], language: Language) -> list[Scope]:
    code_tokens = filter_tokens(tokens)
    nocl_comment_tokens = filter_nocl_comment_tokens(tokens)
    headers = language.extract_headers(code_tokens)
    blocks = language.extract_blocks(code_tokens, headers)
    scopes = _build_scopes_from_headers_and_blocks(
        headers, blocks, language.allow_nested_scopes
    )
    return _filter_nocl_scopes(scopes, nocl_comment_tokens)


def _build_scopes_from_headers_and_blocks(
        headers: list[Header], blocks: list[TokenRange], allow_nested=False
) -> list[Scope]:
    result: list[Scope] = []
    reverse_headers = headers[::-1]
    for header in reverse_headers:
        scope_blocks_indices = _find_scope_blocks_indices(
            header.token_range, blocks, allow_nested
        )
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
        header: TokenRange, blocks: list[TokenRange], allow_nested=False
) -> list[int]:
    body_block = _get_closest_block(header, blocks, allow_nested)
    if body_block:
        if body_block.contains(header):
            return [i for i in range(len(blocks)) if body_block.contains(blocks[i])]
        else:
            return [i for i in range(len(blocks)) if body_block.overlaps(blocks[i])]
    return []


def _get_closest_block(
        header: TokenRange, blocks: list[TokenRange], allow_nested=False
) -> Optional[TokenRange]:
    for block in blocks:
        if not allow_nested and block.contains(header):
            return block
        if block.gt(header):
            return block
    return None


def _filter_nocl_scopes(
        scopes: list[Scope], nocl_comment_tokens: list[Token]
) -> list[Scope]:
    nocl_comment_lines = [t.location.line for t in nocl_comment_tokens]

    def get_scope_header_lines(scope: Scope) -> set[int]:
        result = set([t.location.line for t in scope.header.token_range.tokens])
        first_line = scope.header.token_range.tokens[0].location.line
        if first_line > 0:
            result.add(first_line - 1)
        return result

    return [
        s
        for s in scopes
        if len(get_scope_header_lines(s).intersection(nocl_comment_lines)) == 0
    ]


def has_name_prefix(tokens: list[Token], index: int) -> bool:
    return 0 < index < len(tokens) and tokens[index - 1].is_name()


def has_curly_suffix(tokens: list[Token], index):
    return index < len(tokens) - 1 and tokens[index + 1].is_symbol("{")


def get_headers(tokens: list[Token], pattern: list[TokenPredicate]):
    matches = match(tokens, pattern)
    result = []
    for m in matches:
        name_token = next(t for t in m.tokens if t.is_name())
        if name_token:
            result.append(Header(name_token.value, m))
    return result


def get_blocks(
        tokens: list[Token], open: str, close: str, extract_nested=False
) -> list[TokenRange]:
    balanced_tokens = get_balanced_symbol_token_indices(
        tokens, open, close, extract_nested
    )
    return [TokenRange(tokens[bt[0]: bt[1] + 1]) for bt in balanced_tokens]
