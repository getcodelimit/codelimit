from pygments.lexers import CLexer

from codelimit.common.TokenRange import TokenRange, sort_token_ranges
from codelimit.common.lexer_utils import lex
from codelimit.common.source_utils import get_token_range
from codelimit.common.token_utils import (
    get_balanced_symbol_token_indices,
    get_balanced_symbol_token_ranges, token_string,
)


def test_get_balanced_symbol_token_indices():
    tokens = lex(CLexer(), "void foo() { while (1) { } }")

    result = get_balanced_symbol_token_indices(tokens, "(", ")")

    assert len(result) == 2
    assert result[0][0] == 2
    assert result[0][1] == 3
    assert result[1][0] == 6
    assert result[1][1] == 8

    result = get_balanced_symbol_token_indices(tokens, "{", "}")

    assert len(result) == 1
    assert result[0][0] == 4
    assert result[0][1] == 11

    result = get_balanced_symbol_token_indices(tokens, "{", "}", True)

    assert len(result) == 2
    assert result[0][0] == 9
    assert result[0][1] == 10
    assert result[1][0] == 4
    assert result[1][1] == 11


def test_get_balanced_symbol_token_ranges():
    tokens = lex(CLexer(), "void foo() { while (1) { } }")

    result = get_balanced_symbol_token_ranges(tokens, "{", "}")

    assert len(result) == 2
    assert token_string(tokens, result[0]) == "{ }"
    assert token_string(tokens, result[1]) == "{ while ( 1 ) { } }"


def test_get_token_range():
    code = "void foo() { while (1) { } }"
    tokens = lex(CLexer(), code)

    assert get_token_range(code, tokens[4], tokens[11]) == "{ while (1) { } }"


def test_sort_token_ranges():
    code = ""
    code += "{ { { }\n"
    code += "    { 1\n"
    code += "    }\n"
    code += "  }\n"
    code += "}\n"
    tokens = lex(CLexer(), code)

    token_ranges: list[TokenRange] = [TokenRange(2, 4), TokenRange(4, 7), TokenRange(1, 8), TokenRange(0, 9)]

    result = sort_token_ranges(token_ranges, tokens)

    assert tokens[result[0].start].location.line == 1
    assert tokens[result[0].start].location.column == 1
    assert tokens[result[1].start].location.line == 1
    assert tokens[result[1].start].location.column == 3
    assert tokens[result[2].start].location.line == 1
    assert tokens[result[2].start].location.column == 5
    assert tokens[result[3].start].location.line == 2
    assert tokens[result[3].start].location.column == 5
