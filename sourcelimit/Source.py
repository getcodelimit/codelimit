from sourcelimit.Position import Position


def index_to_position(code: str, index: int) -> Position:
    line = 1 + len([c for c in code[:index] if c == '\n'])
    if code[index - 1] == '\n':
        line -= 1
    column = 0
    for i in range(index - 1, -1, -1):
        c = code[i]
        if c == '\n':
            break
        column += 1
    return Position(line, column)