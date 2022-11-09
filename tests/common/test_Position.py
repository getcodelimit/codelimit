from codelimit.common.SourceLocation import SourceLocation


def test_str():
    position = SourceLocation(1, 1)

    assert str(position) == '{line: 1, column: 1}'
