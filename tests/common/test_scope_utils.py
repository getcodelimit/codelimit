from pygments.lexers import PythonLexer

from codelimit.common.lexer_utils import lex
from codelimit.common.scope.scope_utils import _find_scope_blocks_indices
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
