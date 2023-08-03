from codelimit.common.scope.scope_utils import _find_scope_blocks_indices
from codelimit.languages.python.PythonLaguage import PythonLanguage
from codelimit.languages.python.PythonScopeExtractor import PythonScopeExtractor


def test_find_scope_blocks_indices():
    code = ''
    code += 'def foo():\n'
    code += '  pass\n'
    code += '\n'
    code += 'def bar():\n'
    code += '  foo()\n'

    tokens = PythonLanguage().lex(code)
    extractor = PythonScopeExtractor()
    headers = extractor.extract_headers(tokens)
    blocks = extractor.extract_blocks(tokens, headers)

    assert _find_scope_blocks_indices(headers[0].token_range, blocks) == [0]
    assert _find_scope_blocks_indices(headers[1].token_range, blocks) == [1]
