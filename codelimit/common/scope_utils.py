from codelimit.common.Scope import Scope
from codelimit.common.SourceRange import SourceRange
from codelimit.languages.Language import Language


def build_scopes(language: Language, code: str):
    tokens = language.lex(code)
    scope_extractor = language.get_scope_extractor()
    headers = scope_extractor.extract_headers(code, tokens)
    blocks = scope_extractor.extract_blocks(code, tokens)
    return _build_scopes_from_headers_and_blocks(headers, blocks)


def _build_scopes_from_headers_and_blocks(headers: list[SourceRange], blocks: list[SourceRange]) -> list[Scope]:
    result = []
    reverse_blocks = blocks[::-1]
    for header in headers[::-1]:
        scope_blocks = []
        for index, block in enumerate(reverse_blocks):
            if block.start.line <= header.start.line:
                reverse_blocks = reverse_blocks[index:]
                break
            if block.start.column > header.start.column:
                scope_blocks.append(block)
            else:
                scope_blocks = []
        if len(scope_blocks) > 0:
            scope_block = SourceRange(scope_blocks[-1].start, scope_blocks[0].end)
            result.append(Scope(header, scope_block))
    result.reverse()
    return result
