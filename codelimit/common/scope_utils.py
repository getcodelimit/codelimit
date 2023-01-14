from codelimit.common.Language import Language
from codelimit.common.Scope import Scope
from codelimit.common.TokenRange import TokenRange
from codelimit.common.token_utils import sort_tokens
from codelimit.common.utils import delete_indices


def build_scopes(language: Language, code: str) -> list[Scope]:
    tokens = language.lex(code)
    scope_extractor = language.get_scope_extractor()
    headers = scope_extractor.extract_headers(tokens)
    blocks = scope_extractor.extract_blocks(tokens)
    return _build_scopes_from_headers_and_blocks(headers, blocks)


def _build_scopes_from_headers_and_blocks(headers: list[TokenRange], blocks: list[TokenRange]) -> list[Scope]:
    result: list[Scope] = []
    reverse_headers = headers[::-1]
    for header in reverse_headers:
        scope_blocks_indices = _find_scope_blocks_indices(header, blocks)
        scope_tokens = []
        for i in scope_blocks_indices:
            scope_tokens.extend(blocks[i].tokens)
        scope_tokens = sort_tokens(scope_tokens)
        scope_block = TokenRange(scope_tokens)
        result.append(Scope(header, scope_block))
        blocks = delete_indices(blocks, scope_blocks_indices)
    result.reverse()
    return result


def _find_scope_blocks_indices(header: TokenRange, blocks: list[TokenRange]) -> list[int]:
    blocks_after_header = [i for i in range(len(blocks)) if header.lt(blocks[i])]
    if len(blocks_after_header) > 0:
        body_blocks = [i for i in blocks_after_header if blocks[blocks_after_header[0]].overlaps(blocks[i])]
        return body_blocks
    return []
