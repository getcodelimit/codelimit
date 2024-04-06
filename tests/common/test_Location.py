from codelimit.common.Location import Location


def test_equality():
    loc1 = Location(1, 1)
    loc2 = Location(1, 1)

    assert loc1 == loc2

    loc3 = Location(1, 2)
    loc4 = Location(2, 1)

    assert loc1 != loc3
    assert loc1 != loc4
