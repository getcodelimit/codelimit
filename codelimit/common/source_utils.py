from codelimit.common.Location import Location
from codelimit.common.Token import Token


def get_newline_indices(code: str) -> list[int]:
    result = []
    for index, c in enumerate(code):
        if c == "\n":
            result.append(index)
    return result


def index_to_location(code: str, index: int) -> Location:
    line = 1 + len([c for c in code[: index + 1] if c == "\n"])
    if index > 0 and code[index] == "\n":
        line -= 1
    if index == 0:
        column = 1
    else:
        column = 0
        for i in range(index, -1, -1):
            c = code[i]
            if c == "\n":
                break
            column += 1
    return Location(line, column)


def location_to_index(code: str, position: Location) -> int:
    result = 0
    lines = code.split("\n")
    for i in range(0, position.line - 1):
        result += len(lines[i]) + 1
    result += max(0, position.column - 1)
    return result


def get_token_range(code: str, start: Token, end: Token) -> str:
    start_index = location_to_index(code, start.location)
    end_index = location_to_index(code, end.location)
    return code[start_index : end_index + len(end.value)]


def get_location_range(code: str, start: Location, end: Location) -> str:
    start_index = location_to_index(code, start)
    end_index = location_to_index(code, end)
    return code[start_index:end_index]


def filter_tokens(
    tokens: list[Token], keep_whitespace=False, keep_comments=False, keep_others=True
) -> list[Token]:
    def predicate(token: Token):
        if token.is_whitespace():
            return keep_whitespace
        elif token.is_comment():
            return keep_comments
        else:
            return keep_others

    return [t for t in tokens if predicate(t)]


def filter_nocl_comment_tokens(tokens: list[Token]):
    def predicate(token: Token):
        if token.is_comment():
            value = token.value.lower()
            return value.startswith("#nocl") or value.startswith("# nocl")
        else:
            return False

    return [t for t in tokens if predicate(t)]
