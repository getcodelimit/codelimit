from sourcelimit.Source import index_to_position


def test_index_to_position_single_line():
    code = 'foo = bar'

    result = index_to_position(code, 5)

    assert result.line == 1
    assert result.column == 5


def test_index_to_position_multiline():
    code = ''
    code += 'foo = bar\n'
    code += 'spam = eggs\n'

    result = index_to_position(code, 16)

    assert result.line == 2
    assert result.column == 6


def test_index_to_position_index_is_newline():
    code = ''
    code += 'foo = bar\n'
    code += '\n'

    result = index_to_position(code, 11)

    assert result.line == 2
    assert result.column == 0
