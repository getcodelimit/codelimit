from codelimit.common.Scope import Scope
from codelimit.common.SourceRange import SourceRange


def build_scopes(headers: list[SourceRange], blocks: list[SourceRange]) -> list[Scope]:
    result = []
    reverse_blocks = blocks[::-1]
    for header in headers[::-1]:
        scope_blocks = []
        for index, block in enumerate(reverse_blocks):
            if block.start.line < header.start.line:
                reverse_blocks = reverse_blocks[index:]
                break
            if block.start.column > header.start.column:
                scope_blocks.append(block)
        if len(scope_blocks) > 0:
            scope_block = SourceRange(scope_blocks[-1].start, scope_blocks[0].end)
            result.append(Scope(header, scope_block))
    result.reverse()
    return result
