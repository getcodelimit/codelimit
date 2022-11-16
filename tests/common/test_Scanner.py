import os.path
import tempfile
from pathlib import Path

from codelimit.common.Scanner import scan


def test_scan_single_file():
    tmp_root = tempfile.TemporaryDirectory()
    with open(os.path.join(tmp_root.name, 'foo.py'), 'w') as pythonFile:
        code = ''
        code += 'def foo():\n'
        code += '  return "Hello world"\n'
        pythonFile.write(code)

    result = scan(Path(tmp_root.name))

    assert result.total_loc() == 2
    assert len(result.all_measurements()) == 1
    assert result.all_file_measurements()[0].path == 'foo.py'


def test_scan_single_file_in_sub_folder():
    tmp_root = tempfile.TemporaryDirectory()
    os.mkdir(os.path.join(tmp_root.name, 'src'))
    with open(os.path.join(tmp_root.name, 'src', 'foo.py'), 'w') as pythonFile:
        code = ''
        code += 'def foo():\n'
        code += '  return "Hello world"\n'
        pythonFile.write(code)

    result = scan(Path(tmp_root.name))

    assert result.total_loc() == 2
    assert len(result.all_measurements()) == 1
    assert result.all_file_measurements()[0].path == 'src/foo.py'


def test_skip_hidden_files():
    tmp_root = tempfile.TemporaryDirectory()
    with open(os.path.join(tmp_root.name, 'foo.py'), 'w') as pythonFile:
        code = ''
        code += 'def foo():\n'
        code += '  return "Hello world"\n'
        pythonFile.write(code)
    with open(os.path.join(tmp_root.name, '.bar.py'), 'w') as pythonFile:
        code = ''
        code += 'def bar():\n'
        code += '  return "Hello world"\n'
        pythonFile.write(code)

    path_parts = tmp_root.name.split(os.path.sep)
    path_parts.append('..')
    path_parts.append(path_parts[-2])
    path = Path(str.join(os.path.sep, path_parts))
    result = scan(path)

    assert result.total_loc() == 2
    assert len(result.all_measurements()) == 1
    assert result.all_file_measurements()[0].path == 'foo.py'
