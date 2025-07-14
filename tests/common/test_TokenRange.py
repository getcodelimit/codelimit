from pygments.lexers import CLexer

from codelimit.common.TokenRange import TokenRange
from codelimit.common.lexer_utils import lex
from codelimit.common.token_utils import token_string


def test_token_string():
    tokens = lex(CLexer(), "int main() { { return 0; } }")
    token_range = TokenRange(5, 10)

    assert token_string(tokens, token_range) == "{ return 0 ; }"


def test_contains():
    token_range = TokenRange(0, 11)
    nested_token_range = TokenRange(5, 10)

    assert token_range.contains(nested_token_range)
    assert not nested_token_range.contains(token_range)
    assert not token_range.contains(token_range)

def test_overlaps():
    token_range = TokenRange(4, 10)
    start_overlapping_token_range = TokenRange(0, 5)
    end_overlapping_token_range = TokenRange(8, 11)
    non_overlapping_token_range = TokenRange(1, 3)

    assert start_overlapping_token_range.overlaps(token_range)
    assert token_range.overlaps(start_overlapping_token_range)
    assert end_overlapping_token_range.overlaps(token_range)
    assert token_range.overlaps(end_overlapping_token_range)
    assert not token_range.overlaps(non_overlapping_token_range)

def test_lt_gt():
    header_token_range = TokenRange(0, 4)
    block_token_range = TokenRange(4, 11)

    assert header_token_range.lt(block_token_range)
    assert not block_token_range.lt(header_token_range)
    assert block_token_range.gt(header_token_range)
    assert not header_token_range.gt(block_token_range)
