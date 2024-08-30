import tempfile
from pathlib import Path

from codelimit.commands.check import check_file
from codelimit.common.CheckResult import CheckResult


def test_check_file():
    code = ""
    code += "def foo():\n"
    code += '    print("Hello, world!")\n'
    tmp = tempfile.NamedTemporaryFile(suffix=".py")
    tmp.write(code.encode())
    check_result = CheckResult()

    check_file(Path(tmp.name), check_result)

    assert len(check_result.file_list) == 1


def test_check_unsupported_file():
    tmp = tempfile.NamedTemporaryFile(suffix=".gitignore")
    tmp.write("".encode())
    check_result = CheckResult()

    check_file(Path(tmp.name), check_result)

    assert len(check_result.file_list) == 0
