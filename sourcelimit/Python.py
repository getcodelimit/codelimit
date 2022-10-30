from re import finditer

from sourcelimit.Block import Block
from sourcelimit.Header import Header
from sourcelimit.Position import Position
from sourcelimit.Source import index_to_position


def get_indentation(line: str):
    result = 0
    for c in line:
        if c == ' ':
            result += 1
        elif c == '\t':
            result += 4
        else:
            return result
    return None


def get_blocks(code: str) -> list[Block]:
    result = []
    lines = code.split('\n')
    line_nr = 0
    indentation = None
    start = None
    end = None
    for line in lines:
        line_nr += 1
        line_indentation = get_indentation(line)
        if line_indentation is None:
            break
        end = Position(line_nr, len(line))
        if indentation is None:
            start = Position(line_nr, line_indentation + 1)
        elif line_indentation != indentation:
            result.append(Block(start, end))
        indentation = line_indentation
    if start and indentation is not None:
        result.append(Block(start, end))
    return result


def get_headers(code: str) -> list[Header]:
    result = []
    for match in finditer(r'\b(def)\b', code):
        start_index = match.span(1)[0]
        end_index = match.span(1)[1]
        header = Header(index_to_position(code, start_index), index_to_position(code, end_index))
        result.append(header)
    return result
