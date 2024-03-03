from pygments.lexers import PythonLexer

from codelimit.common.TokenRange import TokenRange
from codelimit.common.lexer_utils import lex
from codelimit.common.scope.Header import Header
from codelimit.common.scope.Scope import Scope


def test_single_line():
    code = 'print("hello world")'
    tokens = lex(PythonLexer(), code)
    scope = Scope(Header("print", TokenRange(tokens[:1])), TokenRange(tokens[1:]))

    assert str(scope) == "[{line: 1, column: 1}, {line: 1, column: 20}]"
    assert len(scope) == 1


def test_multiline():
    code = ""
    code += "def foo():\n"
    code += "  pass\n"
    tokens = lex(PythonLexer(), code)
    scope = Scope(Header("foo", TokenRange(tokens[0:5])), TokenRange(tokens[5:]))

    assert str(scope) == "[{line: 1, column: 1}, {line: 2, column: 3}]"
    assert len(scope) == 2
