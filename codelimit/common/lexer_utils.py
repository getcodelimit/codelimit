from pygments.lexer import Lexer

from codelimit.common.Location import Location
from codelimit.common.Token import Token
from codelimit.common.source_utils import filter_tokens, get_newline_indices


def lex(lexer: Lexer, code: str, filter_comments=True) -> list[Token]:
    lexer_tokens = lexer.get_tokens_unprocessed(code)
    indices = get_newline_indices(code)
    if len(indices) == 0:
        tokens = [Token(Location(1, t[0] + 1), t[1], t[2]) for t in lexer_tokens]
    else:
        tokens = []
        newline_index = 0
        line_start = 0
        for t in lexer_tokens:
            while newline_index < len(indices) and t[0] > indices[newline_index]:
                line_start = indices[newline_index] + 1
                newline_index += 1
            tokens.append(
                Token(Location(newline_index + 1, t[0] - line_start + 1), t[1], t[2])
            )

    if filter_comments:
        return filter_tokens(tokens)
    else:
        return filter_tokens(tokens, keep_comments=True)
