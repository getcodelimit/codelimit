from pygments.lexers import CLexer

from codelimit.common.TokenRange import TokenRange
from codelimit.common.lexer_utils import lex


def test_token_string():
    tokens = lex(CLexer(), "int main() { { return 0; } }")
    token_range = TokenRange(tokens[5:10])

    assert token_range.token_string() == "{ return 0 ; }"


def test_contains():
    tokens = lex(CLexer(), "int main() { { return 0; } }")
    token_range = TokenRange(tokens)
    nested_token_range = TokenRange(tokens[5:10])

    assert token_range.contains(nested_token_range)
    assert not nested_token_range.contains(token_range)
    assert not token_range.contains(token_range)


def test_lt_gt():
    tokens = lex(CLexer(), "int main() { { return 0; } }")
    header_token_range = TokenRange(tokens[0:4])
    block_token_range = TokenRange(tokens[4:11])

    assert header_token_range.lt(block_token_range)
    assert not block_token_range.lt(header_token_range)
    assert block_token_range.gt(header_token_range)
    assert not header_token_range.gt(block_token_range)
