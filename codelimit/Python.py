from re import finditer

from codelimit.Location import Location
from codelimit.Source import index_to_location
from codelimit.SourceRange import Block, Header


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
        end = Location(line_nr, len(line))
        if indentation is None:
            start = Location(line_nr, line_indentation + 1)
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
        c = code[start_index]
        end_index = match.span(1)[1]
        header = Header(index_to_location(code, start_index), index_to_location(code, end_index - 1))
        result.append(header)
    return result
