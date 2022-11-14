from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.SourceRange import SourceRange


def test_str():
    block = SourceRange(SourceLocation(1, 1), SourceLocation(2, 10))

    assert str(block) == '[{line: 1, column: 1}, {line: 2, column: 10}]'

