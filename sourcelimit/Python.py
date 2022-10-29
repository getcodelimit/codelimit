from sourcelimit.Block import Block
from sourcelimit.Position import Position


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
