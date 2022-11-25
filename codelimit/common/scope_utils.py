from codelimit.common.Scope import Scope
from codelimit.common.TokenRange import TokenRange
from codelimit.common.Language import Language


def build_scopes(language: Language, code: str) -> list[Scope]:
    tokens = language.lex(code)
    scope_extractor = language.get_scope_extractor()
    headers = scope_extractor.extract_headers(tokens)
    blocks = scope_extractor.extract_blocks(tokens)
    return _build_scopes_from_headers_and_blocks(headers, blocks)


def _build_scopes_from_headers_and_blocks(headers: list[TokenRange], blocks: list[TokenRange]) -> list[Scope]:
    result = []
    reverse_blocks = blocks[::-1]
    for header in headers[::-1]:
        scope_blocks = []
        for index, block in enumerate(reverse_blocks):
            if block.lt(header) or block.overlaps(header):
                reverse_blocks = reverse_blocks[index:]
                break
            if block.tokens[0].location.column > header.tokens[0].location.column:
                scope_blocks = block.tokens + scope_blocks
            else:
                scope_blocks = []
        if len(scope_blocks) > 0:
            scope_block = TokenRange(scope_blocks)
            result.append(Scope(header, scope_block))
    result.reverse()
    return result
