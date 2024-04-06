from codelimit.common.gsm.predicate.Identity import Identity


def test_equals():
    identity = Identity("a")

    assert identity == identity
    assert Identity(1) == Identity(1)
    assert Identity("a") == Identity("a")
    assert Identity("a") != Identity("b")
