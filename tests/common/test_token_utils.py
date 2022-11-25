from codelimit.common.token_utils import get_balanced_symbol_token_indices
from codelimit.languages.c.CLanguage import CLanguage


def test_get_balanced_symbol_token_indices():
    tokens = CLanguage().lex('void foo() { while (1) { } }')

    result = get_balanced_symbol_token_indices(tokens, '(', ')')

    assert len(result) == 2
    assert result[0][0] == 2
    assert result[0][1] == 3
    assert result[1][0] == 6
    assert result[1][1] == 8

    result = get_balanced_symbol_token_indices(tokens, '{', '}')

    assert len(result) == 1
    assert result[0][0] == 4
    assert result[0][1] == 11

    result = get_balanced_symbol_token_indices(tokens, '{', '}', True)

    assert len(result) == 2
    assert result[0][0] == 9
    assert result[0][1] == 10
    assert result[1][0] == 4
    assert result[1][1] == 11
