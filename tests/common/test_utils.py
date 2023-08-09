import os
import tempfile

from codelimit.common.utils import (
    path_has_extension,
    get_parent_folder,
    get_basename,
    delete_indices,
    calculate_checksum,
)


def test_path_has_extension():
    assert path_has_extension("foo.c", ["c"])
    assert path_has_extension("foo.c", "c")
    assert path_has_extension("foo.c", ["h"]) is False
    assert path_has_extension("foo.c", "h") is False
    assert path_has_extension("foo.", ["c"]) is False
    assert path_has_extension("foo", ["c"]) is False


def test_get_parent_folder():
    assert get_parent_folder("foo/bar.py") == "foo"
    assert get_parent_folder("foo/bar/span/eggs.py") == "foo/bar/span"
    assert get_parent_folder("foo.py") == "."


def test_get_basename():
    assert get_basename("foo/bar.py") == "bar.py"
    assert get_basename("foo/bar/span/eggs.py") == "eggs.py"
    assert get_basename("foo.py") == "foo.py"


def test_calculate_checksum():
    tmp_root = tempfile.TemporaryDirectory()
    file_path = os.path.join(tmp_root.name, "foo.py")
    with open(file_path, "w") as pythonFile:
        code = ""
        code += "def foo():\n"
        code += '  return "Hello world"\n'
        pythonFile.write(code)

    assert calculate_checksum(file_path) == "b3029c205e58fa4dfb6656d5e8f7a381"


def test_delete_indices():
    collection = [1, 2, 3, 4, 5]

    assert delete_indices(collection, [1, 3]) == [1, 3, 5]
