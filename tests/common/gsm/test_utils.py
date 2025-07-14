from codelimit.common.TokenRange import TokenRange
from codelimit.common.gsm.utils import prune_nested


def test_prune_nested_simple():
    tr1 = TokenRange(0, 5)
    tr2 = TokenRange(6, 10)
    tr3 = TokenRange(11, 15)
    ranges = [tr1, tr2, tr3]

    result = prune_nested(ranges)

    assert len(result) == 3


def test_prune_nested_with_contains():
    tr1 = TokenRange(2, 5)
    tr2 = TokenRange(1, 10)
    tr3 = TokenRange(11, 15)
    ranges = [tr1, tr2, tr3]

    result = prune_nested(ranges)

    assert len(result) == 2
    assert result[0] == tr2
    assert result[1] == tr3


def test_prune_nested_with_overlap():
    tr1 = TokenRange(1, 5)
    tr2 = TokenRange(1, 10)
    tr3 = TokenRange(11, 15)
    ranges = [tr1, tr2, tr3]

    result = prune_nested(ranges)

    assert len(result) == 2
    assert result[0] == tr2
    assert result[1] == tr3


def test_prune_nested_unsorted():
    tr1 = TokenRange(1, 10)
    tr2 = TokenRange(2, 5)
    tr3 = TokenRange(11, 15)
    ranges = [tr1, tr2, tr3]

    result = prune_nested(ranges)

    assert len(result) == 2
    assert result[0] == tr1
    assert result[1] == tr3
