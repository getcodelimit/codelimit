from pygments.lexers import PythonLexer

from codelimit.common.TokenRange import TokenRange
from codelimit.common.lexer_utils import lex


def test_str():
    tokens = lex(PythonLexer(), 'print("hello world"')
    block = TokenRange(tokens)

    assert str(block) == "[{line: 1, column: 1}, {line: 1, column: 19}]"
