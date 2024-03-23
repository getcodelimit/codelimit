from pygments.lexers import JavascriptLexer
from pygments.lexers import PythonLexer

from codelimit.common.TokenRange import TokenRange
from codelimit.common.lexer_utils import lex
from codelimit.common.scope.Header import Header
from codelimit.common.scope.Scope import Scope
from codelimit.common.scope.scope_utils import _find_scope_blocks_indices, fold_scopes
from codelimit.languages.Python import Python


def test_find_scope_blocks_indices():
    code = ""
    code += "def foo():\n"
    code += "  pass\n"
    code += "\n"
    code += "def bar():\n"
    code += "  foo()\n"

    tokens = lex(PythonLexer(), code)
    extractor = Python()
    headers = extractor.extract_headers(tokens)
    blocks = extractor.extract_blocks(tokens, headers)

    assert _find_scope_blocks_indices(headers[0].token_range, blocks) == [0]
    assert _find_scope_blocks_indices(headers[1].token_range, blocks) == [1]


def test_fold_scopes():
    code = ""
    code += "function foo() {\n"
    code += "  function bar() {\n"
    code += "  }\n"
    code += "  bar();\n"
    code += "}\n"
    code += "function foobar() {\n"
    code += "}\n"

    tokens = lex(JavascriptLexer(), code)

    outer_scope = Scope(
        Header("foo", TokenRange(tokens[0:4])), TokenRange(tokens[4:16])
    )
    inner_scope = Scope(
        Header("bar", TokenRange(tokens[5:9])), TokenRange(tokens[9:11])
    )
    next_scope = Scope(
        Header("foobar", TokenRange(tokens[16:20])), TokenRange(tokens[20:])
    )

    result = fold_scopes([outer_scope, inner_scope, next_scope])

    assert len(result) == 2
    assert len(result[0]) == 3
    assert len(result[0].children[0]) == 2
    assert len(result[1]) == 2
