from typing import Callable

from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange


def get_newline_indices(code: str) -> list[int]:
    result = []
    for index, c in enumerate(code):
        if c == '\n':
            result.append(index)
    return result


def index_to_location(code: str, index: int) -> SourceLocation:
    line = 1 + len([c for c in code[:index + 1] if c == '\n'])
    if index > 0 and code[index] == '\n':
        line -= 1
    if index == 0:
        column = 1
    else:
        column = 0
        for i in range(index, -1, -1):
            c = code[i]
            if c == '\n':
                break
            column += 1
    return SourceLocation(line, column)


def location_to_index(code: str, position: SourceLocation) -> int:
    result = 0
    lines = code.split('\n')
    for i in range(0, position.line - 1):
        result += len(lines[i]) + 1
    result += max(0, position.column - 1)
    return result


def get_range(code: str, source_range: TokenRange) -> str:
    start_index = location_to_index(code, source_range.tokens[0].location)
    end_index = location_to_index(code, source_range.tokens[-1].location)
    return code[start_index:end_index + len(source_range.tokens[-1].value)]


def filter_tokens(tokens: list[Token], predicate: Callable[[Token], bool]) -> list[Token]:
    return [t for t in tokens if predicate(t)]
