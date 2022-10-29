from sourcelimit.Block import Block
from sourcelimit.Position import Position


def test_str():
    block = Block(Position(1, 1), Position(2, 10))

    assert str(block) == '[{line: 1, column: 1}, {line: 2, column: 10}]'

