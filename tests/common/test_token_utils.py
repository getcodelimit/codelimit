from pygments.lexers import CLexer

from codelimit.common.TokenRange import TokenRange
from codelimit.common.lexer_utils import lex
from codelimit.common.source_utils import get_token_range
from codelimit.common.token_utils import (
    get_balanced_symbol_token_indices,
    sort_token_ranges,
    get_balanced_symbol_token_ranges,
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
    assert result[0].token_string() == "{ }"
    assert result[1].token_string() == "{ while ( 1 ) }"


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

    token_ranges: list[TokenRange] = []
    token_ranges.append(TokenRange(tokens[2:4]))
    token_ranges.append(TokenRange(tokens[4:7]))
    token_ranges.append(TokenRange(tokens[1:8]))
    token_ranges.append(TokenRange(tokens[0:]))

    result = sort_token_ranges(token_ranges)

    assert result[0].tokens[0].location.line == 1
    assert result[0].tokens[0].location.column == 1
    assert result[1].tokens[0].location.line == 1
    assert result[1].tokens[0].location.column == 3
    assert result[2].tokens[0].location.line == 1
    assert result[2].tokens[0].location.column == 5
    assert result[3].tokens[0].location.line == 2
    assert result[3].tokens[0].location.column == 5
