from pygments.token import Keyword

from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.Token import Token


def test_to_string():
    token = Token(SourceLocation(1, 1), Keyword, 'def')

    assert str(token) == 'def'
