from codelimit.Location import Location
from codelimit.SourceRange import Block


def test_str():
    block = Block(Location(1, 1), Location(2, 10))

    assert str(block) == '[{line: 1, column: 1}, {line: 2, column: 10}]'

