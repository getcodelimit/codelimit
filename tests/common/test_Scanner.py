import os.path
import tempfile
from pathlib import Path

from pathspec import PathSpec

from codelimit.common.Scanner import scan_codebase, is_excluded, DEFAULT_EXCLUDES
from codelimit.common.source_utils import get_location_range


def test_scan_single_file():
    tmp_root = tempfile.TemporaryDirectory()
    with open(os.path.join(tmp_root.name, "foo.py"), "w") as pythonFile:
        code = ""
        code += "def foo():\n"
        code += '  return "Hello world"\n'
        pythonFile.write(code)

    result = scan_codebase(Path(tmp_root.name))

    assert result.total_loc() == 2
    assert len(result.all_measurements()) == 1
    assert result.all_files()[0] == "foo.py"

    m = result.all_measurements()[0]
    snippet = get_location_range(code, m.start, m.end)

    expe = ""
    expe += "def foo():\n"
    expe += '  return "Hello world"'

    assert snippet == expe


def test_scan_unsupported_file():
    tmp_root = tempfile.TemporaryDirectory()
    with open(os.path.join(tmp_root.name, "foo.not-supported"), "w") as pythonFile:
        pythonFile.write("")

    result = scan_codebase(Path(tmp_root.name))

    assert len(result.all_files()) == 0


def test_scan_single_file_in_sub_folder():
    tmp_root = tempfile.TemporaryDirectory()
    os.mkdir(os.path.join(tmp_root.name, "src"))
    with open(os.path.join(tmp_root.name, "src", "foo.py"), "w") as pythonFile:
        code = ""
        code += "def foo():\n"
        code += '  return "Hello world"\n'
        pythonFile.write(code)

    result = scan_codebase(Path(tmp_root.name))

    assert result.total_loc() == 2
    assert len(result.all_measurements()) == 1
    assert result.all_files()[0] == "src/foo.py"


def test_skip_hidden_files():
    tmp_root = tempfile.TemporaryDirectory()
    with open(os.path.join(tmp_root.name, "foo.py"), "w") as pythonFile:
        code = ""
        code += "def foo():\n"
        code += '  return "Hello world"\n'
        pythonFile.write(code)
    with open(os.path.join(tmp_root.name, ".bar.py"), "w") as pythonFile:
        code = ""
        code += "def bar():\n"
        code += '  return "Hello world"\n'
        pythonFile.write(code)

    path_parts = tmp_root.name.split(os.path.sep)
    path_parts.append("..")
    path_parts.append(path_parts[-2])
    path = Path(str.join(os.path.sep, path_parts))
    result = scan_codebase(path)

    assert result.total_loc() == 2
    assert len(result.all_measurements()) == 1
    assert result.all_files()[0] == "foo.py"


def test_is_excluded():
    excludes_spec = PathSpec.from_lines("gitignore", DEFAULT_EXCLUDES)

    assert is_excluded(Path("venv/foo/bar.py"), excludes_spec)
    assert is_excluded(Path("tests/test_utils.py"), excludes_spec)
    assert not is_excluded(Path("foo/bar.py"), excludes_spec)

    excludes_spec = PathSpec.from_lines("gitignore", ["output"])

    assert is_excluded(Path("output/foo/bar.py"), excludes_spec)
    assert not is_excluded(Path("venv/foo/bar.py"), excludes_spec)
    assert not is_excluded(Path("foo/bar.py"), excludes_spec)

    excludes_spec = PathSpec.from_lines("gitignore", ["foo/bar/*"])

    assert is_excluded(Path("foo/bar/foobar.py"), excludes_spec)

    excludes_spec = PathSpec.from_lines("gitignore", ["site/"])

    assert is_excluded(Path("site/assets/javascripts/lunr/wordcut.js"), excludes_spec)

    excludes_spec = PathSpec.from_lines("gitignore", ["!site/"])

    assert not is_excluded(
        Path("site/assets/javascripts/lunr/wordcut.js"), excludes_spec
    )
