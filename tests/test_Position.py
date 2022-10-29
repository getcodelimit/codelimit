from sourcelimit.Position import Position


def test_str():
    position = Position(1, 1)

    assert str(position) == '{line: 1, column: 1}'
