from codelimit.common.Location import Location


def test_str():
    position = Location(1, 1)

    assert str(position) == "{line: 1, column: 1}"
