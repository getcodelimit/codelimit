from codelimit.Location import Location
from codelimit.SourceRange import SourceRange


def index_to_location(code: str, index: int) -> Location:
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
    return Location(line, column)


def location_to_index(code: str, position: Location) -> int:
    result = 0
    lines = code.split('\n')
    for i in range(0, position.line - 1):
        result += len(lines[i]) + 1
    result += max(0, position.column - 1)
    return result


def get_range(code: str, source_range: SourceRange) -> str:
    start_index = location_to_index(code, source_range.start)
    end_index = location_to_index(code, source_range.end)
    return code[start_index:end_index + 1]
