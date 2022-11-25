from codelimit.common.utils import path_has_suffix


def test_path_has_suffix():
    assert path_has_suffix('foo.c', ['c'])
    assert path_has_suffix('foo.c', 'c')
    assert path_has_suffix('foo.c', ['h']) is False
    assert path_has_suffix('foo.c', 'h') is False
    assert path_has_suffix('foo.', ['c']) is False
    assert path_has_suffix('foo', ['c']) is False
