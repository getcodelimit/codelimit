from pygments.lexers import JavascriptLexer
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


def test_children():
    code = ""
    code += "function foo() {\n"
    code += "  function bar() {\n"
    code += "  }\n"
    code += "  bar();\n"
    code += "}\n"

    tokens = lex(JavascriptLexer(), code)

    outer_scope = Scope(Header("foo", TokenRange(tokens[0:4])), TokenRange(tokens[4:]))
    inner_scope = Scope(
        Header("bar", TokenRange(tokens[5:9])), TokenRange(tokens[9:11])
    )

    outer_scope.children.append(inner_scope)

    assert len(inner_scope) == 2
    assert len(outer_scope) == 3


def test_contains():
    code = ""
    code += "function foo() {\n"
    code += "  function bar() {\n"
    code += "  }\n"
    code += "  bar();\n"
    code += "}\n"

    tokens = lex(JavascriptLexer(), code)

    outer_scope = Scope(Header("foo", TokenRange(tokens[0:4])), TokenRange(tokens[4:]))
    inner_scope = Scope(
        Header("bar", TokenRange(tokens[5:9])), TokenRange(tokens[9:11])
    )

    assert outer_scope.contains(inner_scope)
    assert not inner_scope.contains(outer_scope)
