from sourcelimit.Python import get_indentation, get_blocks


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