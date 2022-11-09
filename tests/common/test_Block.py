from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.SourceRange import Block


def test_str():
    block = Block(SourceLocation(1, 1), SourceLocation(2, 10))

    assert str(block) == '[{line: 1, column: 1}, {line: 2, column: 10}]'

