from typing import Optional

from codelimit.common.Language import Language
from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange, sort_token_ranges
from codelimit.common.gsm.Expression import Expression
from codelimit.common.gsm.matcher import find_all, starts_with
from codelimit.common.scope.Header import Header, sort_headers
from codelimit.common.scope.Scope import Scope
from codelimit.common.source_utils import filter_tokens, filter_nocl_comment_tokens
from codelimit.common.token_utils import get_balanced_symbol_token_indices
from codelimit.common.utils import delete_indices


def build_scopes(tokens: list[Token], language: Language) -> list[Scope]:
    code_tokens = filter_tokens(tokens)
    nocl_comment_tokens = filter_nocl_comment_tokens(tokens)
    headers = language.extract_headers(code_tokens)
    blocks = language.extract_blocks(code_tokens, headers)
    scopes = _build_scopes_from_headers_and_blocks(headers, blocks, code_tokens)
    filtered_scopes = _filter_nocl_scopes(scopes, nocl_comment_tokens)
    if language.allow_nested_functions:
        return fold_scopes(filtered_scopes)
    else:
        return filter_scopes_nested_functions(filtered_scopes)


def fold_scopes(scopes: list[Scope]) -> list[Scope]:
    result: list[Scope] = []
    for scope in scopes:
        if len(result) == 0:
            result.append(scope)
        else:
            last_scope = result[-1]
            if last_scope.contains(scope):
                last_scope.children.append(scope)
            else:
                result.append(scope)
    return result


def unfold_scopes(scopes: list[Scope]) -> list[Scope]:
    result = []
    for scope in scopes:
        result.append(scope)
        result.extend(unfold_scopes(scope.children))
    return result


def filter_scopes_nested_functions(scopes: list[Scope]) -> list[Scope]:
    result: list[Scope] = []
    for scope in scopes:
        if len(result) == 0:
            result.append(scope)
        else:
            last_scope = result[-1]
            if last_scope.contains(scope):
                continue
            else:
                result.append(scope)
    return result


def _build_scopes_from_headers_and_blocks(
        headers: list[Header], blocks: list[TokenRange], tokens: list[Token]
) -> list[Scope]:
    result: list[Scope] = []
    reverse_headers = sort_headers(headers, tokens, reverse=True)
    for header in reverse_headers:
        scope_blocks_indices = _find_scope_blocks_indices(header.token_range, blocks)
        if len(scope_blocks_indices) > 0:
            start = min(blocks[bi].start for bi in scope_blocks_indices)
            end = max(blocks[bi].end for bi in scope_blocks_indices)
            result.append(Scope(header, TokenRange(start, end)))
            blocks = delete_indices(blocks, scope_blocks_indices)
    result.reverse()
    return result


def _find_scope_blocks_indices(
        header: TokenRange, blocks: list[TokenRange]
) -> list[int]:
    body_block = _get_nearest_block(header, blocks)
    if body_block:
        if body_block.contains(header):
            return [i for i in range(len(blocks)) if body_block.contains(blocks[i])]
        else:
            return [i for i in range(len(blocks)) if body_block.overlaps(blocks[i])]
    return []


def _get_nearest_block(
        header: TokenRange, blocks: list[TokenRange]
) -> Optional[TokenRange]:
    reverse_blocks = blocks[::-1]
    result = None
    for block in reverse_blocks:
        if block.contains(header):
            return block if not result else result
        elif block.gt(header):
            result = block
        elif block.lt(header):
            break
    return result


def _filter_nocl_scopes(
        scopes: list[Scope], nocl_comment_tokens: list[Token]
) -> list[Scope]:
    nocl_comment_lines = [t.location.line for t in nocl_comment_tokens]
    return [s for s in scopes if s.header.name_token.location.line not in nocl_comment_lines]


def has_name_prefix(tokens: list[Token], index: int) -> bool:
    return 0 < index < len(tokens) and tokens[index - 1].is_name()


def has_curly_suffix(tokens: list[Token], index):
    return index < len(tokens) - 1 and tokens[index + 1].is_symbol("{")


def get_headers(
        tokens: list[Token], expression: Expression, followed_by: Expression = None, nested: bool = False
) -> list[Header]:
    # expression = replace_string_literal_with_predicate(expression)
    patterns = find_all(expression, tokens, nested=nested)
    if followed_by:
        patterns = [p for p in patterns if starts_with(followed_by, tokens[p.end:])]
    result = []
    for pattern in patterns:
        name_token = next(t for t in pattern.tokens if t.is_name())
        if name_token:
            result.append(Header(name_token, TokenRange(pattern.start, pattern.end)))
    return result


def get_blocks(
        tokens: list[Token], open: str, close: str, extract_nested: bool = True
) -> list[TokenRange]:
    balanced_tokens = get_balanced_symbol_token_indices(
        tokens, open, close, extract_nested
    )
    token_ranges = [TokenRange(bt[0], bt[1] + 1) for bt in balanced_tokens]
    return sort_token_ranges(token_ranges, tokens)


def count_lines(scope: Scope, tokens: list[Token]):
    return len(set([t.location.line for t in _scope_tokens(scope, tokens)]))


def _scope_tokens(scope: Scope, tokens: list[Token]) -> list[Token]:
    result = []
    children_token_ranges = []
    for child in scope.children:
        children_token_ranges.append(TokenRange(child.header.token_range.start, child.block.end))
    children_token_ranges = sort_token_ranges(children_token_ranges, tokens)
    for index in range(scope.header.token_range.start, scope.block.end):
        while len(children_token_ranges) > 0 and index > children_token_ranges[0].end:
            children_token_ranges.pop(0)
        if len(children_token_ranges) == 0 or index < children_token_ranges[0].start:
            result.append(tokens[index])
    return result
