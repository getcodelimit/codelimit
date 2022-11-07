import os.path
import tempfile

from codelimit.common.Scanner import scan


def test_scan_single_file():
    tmp_root = tempfile.TemporaryDirectory()
    with open(os.path.join(tmp_root.name, 'foo.py'), 'w') as pythonFile:
        code = ''
        code += 'def foo():\n'
        code += '  return "Hello world"\n'
        pythonFile.write(code)

    result = scan(tmp_root.name)

    assert result.total_loc() == 2
    assert len(result.all()) == 1
    assert result.all()[0].filename == 'foo.py'


def test_scan_single_file_in_sub_folder():
    tmp_root = tempfile.TemporaryDirectory()
    os.mkdir(os.path.join(tmp_root.name, 'src'))
    with open(os.path.join(tmp_root.name, 'src', 'foo.py'), 'w') as pythonFile:
        code = ''
        code += 'def foo():\n'
        code += '  return "Hello world"\n'
        pythonFile.write(code)

    result = scan(tmp_root.name)

    assert result.total_loc() == 2
    assert len(result.all()) == 1
    assert result.all()[0].filename == 'src/foo.py'
