from codelimit.languages.python.Python import get_indentation, get_blocks, get_headers


def test_get_indentation():
    assert get_indentation('foo = True') == 0
    assert get_indentation(' foo = True') == 1
    assert get_indentation('    foo = True') == 4
    assert get_indentation('\tfoo = True') == 4
    assert get_indentation('\t \t foo = True') == 10
    assert get_indentation('') is None
    assert get_indentation('  ') is None
    assert get_indentation('\t') is None


def test_get_blocks_no_block():
    code = ''

    result = get_blocks(code)

    assert len(result) == 0


def test_get_blocks_single_block():
    code = 'foo = bar'

    result = get_blocks(code)

    assert len(result) == 1
    assert result[0].start.line == 1
    assert result[0].start.column == 1
    assert result[0].end.line == 1
    assert result[0].end.column == 9


def test_get_blocks_single_multiline_block():
    code = ''
    code += 'foo = bar\n'
    code += 'spam = eggs\n'

    result = get_blocks(code)

    assert len(result) == 1
    assert result[0].start.line == 1
    assert result[0].start.column == 1
    assert result[0].end.line == 2
    assert result[0].end.column == 11


def test_get_headers_no_headers():
    result = get_headers('')

    assert len(result) == 0


def test_get_headers_single_header():
    code = ''
    code += 'def foo():\n'
    code += '  pass\n'

    result = get_headers(code)

    assert len(result) == 1
    assert result[0].start.line == 1
    assert result[0].start.column == 1
    assert result[0].end.line == 1
    assert result[0].end.column == 3


def test_get_headers_multi_header():
    code = ''
    code += 'def foo():\n'
    code += '  pass\n'
    code += '\n'
    code += 'def bar():\n'
    code += '  foo()\n'

    result = get_headers(code)

    assert len(result) == 2
    assert result[1].start.line == 4
    assert result[1].start.column == 1
    assert result[1].end.line == 4
    assert result[1].end.column == 3


def test_get_blocks_multi_blocks():
    code = ''
    code += 'def foo():\n'
    code += '  pass\n'
    code += '\n'
    code += 'def bar():\n'
    code += '  foo()\n'

    result = get_blocks(code)

    assert len(result) == 4
    assert result[0].start.line == 1
    assert result[0].end.line == 1
    assert result[1].start.line == 2
    assert result[1].end.line == 2
    assert result[2].start.line == 4
    assert result[2].end.line == 4
    assert result[3].start.line == 5
    assert result[3].end.line == 5
