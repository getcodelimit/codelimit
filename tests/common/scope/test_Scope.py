from pygments.lexers import JavascriptLexer
from pygments.lexers import PythonLexer

from codelimit.common.TokenRange import TokenRange
from codelimit.common.lexer_utils import lex
from codelimit.common.scope.Header import Header
from codelimit.common.scope.Scope import Scope
from codelimit.common.scope.scope_utils import count_lines


def test_single_line():
    code = 'print("hello world")'
    tokens = lex(PythonLexer(), code)
    scope = Scope(Header("print", TokenRange(0, 1)), TokenRange(1, 6))

    assert str(scope) == "(0, 6)"
    assert count_lines(scope, tokens) == 1


def test_multiline():
    code = ""
    code += "def foo():\n"
    code += "  pass\n"
    tokens = lex(PythonLexer(), code)
    scope = Scope(Header("foo", TokenRange(0, 5)), TokenRange(5, 6))

    assert str(scope) == "(0, 6)"
    assert count_lines(scope, tokens) == 2


def test_children():
    code = ""
    code += "function foo() {\n"
    code += "  function bar() {\n"
    code += "  }\n"
    code += "  bar();\n"
    code += "}\n"

    tokens = lex(JavascriptLexer(), code)

    outer_scope = Scope(Header("foo", TokenRange(0, 4)), TokenRange(4, 16))
    inner_scope = Scope(Header("bar", TokenRange(5, 9)), TokenRange(9, 11))

    outer_scope.children.append(inner_scope)

    assert count_lines(inner_scope, tokens) == 2
    assert count_lines(outer_scope, tokens) == 3


def test_contains():
    outer_scope = Scope(Header("foo", TokenRange(0, 4)), TokenRange(4, 16))
    inner_scope = Scope(Header("bar", TokenRange(5, 9)), TokenRange(9, 11))

    assert outer_scope.contains(inner_scope)
    assert not inner_scope.contains(outer_scope)
