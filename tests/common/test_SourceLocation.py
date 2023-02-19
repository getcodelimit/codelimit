from codelimit.common.Location import Location


def test_lt():
    l1 = Location(1, 1)
    l2 = Location(3, 1)
    l3 = Location(3, 3)

    assert not l1.lt(l1)
    assert l1.lt(l2)
    assert not l2.lt(l1)
    assert l2.lt(l3)
    assert not l3.lt(l2)


def test_le():
    l1 = Location(1, 2)
    l2 = Location(3, 1)
    l3 = Location(3, 3)

    assert l1.le(l1)
    assert l1.le(l2)
    assert not l2.le(l1)
    assert l2.le(l3)
    assert not l3.le(l2)


def test_gt():
    l1 = Location(1, 1)
    l2 = Location(3, 1)
    l3 = Location(3, 3)

    assert not l1.gt(l1)
    assert l2.gt(l1)
    assert not l1.gt(l2)
    assert l3.gt(l2)
    assert not l2.gt(l3)


def test_ge():
    l1 = Location(1, 2)
    l2 = Location(3, 1)
    l3 = Location(3, 3)

    assert l1.ge(l1)
    assert l2.ge(l1)
    assert not l1.ge(l2)
    assert l3.ge(l2)
    assert not l2.ge(l3)
