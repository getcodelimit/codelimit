from codelimit.common.utils import path_has_suffix, get_parent_folder, get_basename, delete_indices


def test_path_has_suffix():
    assert path_has_suffix('foo.c', ['c'])
    assert path_has_suffix('foo.c', 'c')
    assert path_has_suffix('foo.c', ['h']) is False
    assert path_has_suffix('foo.c', 'h') is False
    assert path_has_suffix('foo.', ['c']) is False
    assert path_has_suffix('foo', ['c']) is False


def test_get_parent_folder():
    assert get_parent_folder('foo/bar.py') == 'foo'
    assert get_parent_folder('foo/bar/span/eggs.py') == 'foo/bar/span'
    assert get_parent_folder('foo.py') == '.'


def test_get_basename():
    assert get_basename('foo/bar.py') == 'bar.py'
    assert get_basename('foo/bar/span/eggs.py') == 'eggs.py'
    assert get_basename('foo.py') == 'foo.py'


def test_delete_indices():
    collection = [1, 2, 3, 4, 5]

    assert delete_indices(collection, [1, 3]) == [1, 3, 5]
