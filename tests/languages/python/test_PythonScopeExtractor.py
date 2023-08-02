from codelimit.common.scope.scope_utils import build_scopes
from codelimit.languages.python.PythonLaguage import PythonLanguage
from codelimit.languages.python.PythonScopeExtractor import _get_indentation, PythonScopeExtractor, _get_token_lines


def test_get_indentation():
    assert _get_indentation('foo = True') == 0
    assert _get_indentation(' foo = True') == 1
    assert _get_indentation('    foo = True') == 4
    assert _get_indentation('\tfoo = True') == 4
    assert _get_indentation('\t \t foo = True') == 10
    assert _get_indentation('') is None
    assert _get_indentation('  ') is None
    assert _get_indentation('\t') is None


def test_get_blocks_no_block():
    code = ''

    tokens = PythonLanguage().lex(code)
    result = PythonScopeExtractor().extract_blocks(tokens)

    assert len(result) == 0


def test_get_blocks_single_block():
    code = 'foo = bar'

    tokens = PythonLanguage().lex(code)
    result = PythonScopeExtractor().extract_blocks(tokens)

    assert len(result) == 1
    assert result[0].tokens[0].location.line == 1
    assert result[0].tokens[0].location.column == 1
    assert result[0].tokens[-1].location.line == 1
    assert result[0].tokens[-1].location.column == 7


def test_get_blocks_single_multiline_block():
    code = ''
    code += 'foo = bar\n'
    code += 'spam = eggs\n'

    tokens = PythonLanguage().lex(code)
    result = PythonScopeExtractor().extract_blocks(tokens)

    assert len(result) == 1
    assert result[0].tokens[0].location.line == 1
    assert result[0].tokens[0].location.column == 1
    assert result[0].tokens[-1].location.line == 2
    assert result[0].tokens[-1].location.column == 8


def test_get_blocks_multi_blocks():
    code = ''
    code += 'def foo():\n'
    code += '  pass\n'
    code += '\n'
    code += 'def bar():\n'
    code += '  foo()\n'

    tokens = PythonLanguage().lex(code)
    result = PythonScopeExtractor().extract_blocks(tokens)

    assert len(result) == 4
    assert result[0].tokens[0].location.line == 1
    assert result[0].tokens[-1].location.line == 1
    assert result[1].tokens[0].location.line == 2
    assert result[1].tokens[-1].location.line == 2
    assert result[2].tokens[0].location.line == 4
    assert result[2].tokens[-1].location.line == 4
    assert result[3].tokens[0].location.line == 5
    assert result[3].tokens[-1].location.line == 5


def test_trailing_global_code():
    code = ''
    code += 'def foo():\n'
    code += '  pass\n'
    code += '\n'
    code += 'bar = [\n'
    code += '  "bar"\n'
    code += ']\n'

    result = build_scopes(PythonLanguage(), code)

    assert len(result) == 1
    assert len(result[0]) == 2


def test_get_headers_no_headers():
    tokens = PythonLanguage().lex('')
    result = PythonScopeExtractor().extract_headers(tokens)

    assert len(result) == 0


def test_get_headers_single_header():
    code = ''
    code += 'def foo():\n'
    code += '  pass\n'

    tokens = PythonLanguage().lex(code)
    result = PythonScopeExtractor().extract_headers(tokens)

    assert len(result) == 1
    assert result[0].token_range[0].location.line == 1
    assert result[0].token_range[0].location.column == 1
    assert result[0].token_range[-1].location.line == 1
    assert result[0].token_range[-1].location.column == 9
    assert result[0].name == 'foo'


def test_get_headers_multi_header():
    code = ''
    code += 'def foo():\n'
    code += '  pass\n'
    code += '\n'
    code += 'def bar():\n'
    code += '  foo()\n'

    tokens = PythonLanguage().lex(code)
    result = PythonScopeExtractor().extract_headers(tokens)

    assert len(result) == 2
    assert result[1].token_range[0].location.line == 4
    assert result[1].token_range[0].location.column == 1
    assert result[1].token_range[-1].location.line == 4
    assert result[1].token_range[-1].location.column == 8


def test_get_headers_multi_header_with_comment():
    code = ''
    code += '# def old_foo():\n'
    code += 'def foo():\n'
    code += '  pass\n'
    code += '\n'
    code += 'def bar():\n'
    code += '  foo()\n'

    tokens = PythonLanguage().lex(code)
    result = PythonScopeExtractor().extract_headers(tokens)

    assert len(result) == 2
    assert result[0].token_range[0].location.line == 2
    assert result[0].token_range[0].location.column == 1
    assert result[0].token_range[-1].location.line == 2
    assert result[0].token_range[-1].location.column == 9
    assert result[1].name == 'bar'


def test_do_not_count_comment_lines():
    code = ''
    code += 'def foo():\n'
    code += '# This is a comment\n'
    code += '  pass\n'
    code += '  # This is also a comment\n'

    result = build_scopes(PythonLanguage(), code)

    assert len(result) == 1
    assert len(result[0]) == 2


def test_header_type_hints():
    code = ''
    code += 'def foo(\n'
    code += '  bar: str\n'
    code += ') -> FooBar:\n'
    code += '  pass\n'

    tokens = PythonLanguage().lex(code)
    result = PythonScopeExtractor().extract_headers(tokens)

    assert len(result) == 1
    assert result[0].token_range.token_string() == 'def foo ( bar : str )'


def test_line_continuation():
    code = ''
    code += 'def say_hello():\n'
    code += '  print(\\\n'
    code += '"Hello " +\\\n'
    code += '"world")\n'

    result = build_scopes(PythonLanguage(), code)

    assert len(result) == 1
    assert len(result[0]) == 4


def test_get_token_lines():
    code = ''
    code += 'def foo():\n'
    code += '  pass\n'

    result = _get_token_lines(PythonLanguage().lex(code))

    assert len(result) == 2
    assert str(result[0]) == '[def, foo, (, ), :]'
    assert str(result[1]) == '[pass]'
