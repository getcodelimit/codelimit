from sourcelimit.Location import Location
from sourcelimit.Source import index_to_location, location_to_index


def test_index_to_location_single_line():
    code = 'foo = bar'

    result = index_to_location(code, 5)

    assert result.line == 1
    assert result.column == 6


def test_index_to_location_multiline():
    code = ''
    code += 'foo = bar\n'
    code += 'spam = eggs\n'

    result = index_to_location(code, 16)

    assert result.line == 2
    assert result.column == 7


def test_index_to_location_index_is_newline():
    code = ''
    code += 'foo = bar\n'
    code += '\n'

    result = index_to_location(code, 10)

    assert result.line == 2
    assert result.column == 0


def test_location_to_index():
    code = 'foo = bar'

    result = location_to_index(code, Location(1, 5))

    assert result == 5


def test_location_to_index_multiline():
    code = ''
    code += 'foo = bar\n'
    code += 'spam = eggs\n'

    result = location_to_index(code, Location(2, 6))

    assert result == 16


def test_location_to_index_location_is_newline():
    code = ''
    code += 'foo = bar\n'
    code += '\n'

    result = location_to_index(code, Location(2, 0))

    assert result == 11
