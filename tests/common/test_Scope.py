from codelimit.common.Scope import Scope
from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.SourceRange import SourceRange


def test_single_line():
    scope = Scope(SourceRange(SourceLocation(1, 1), SourceLocation(1, 3)),
                  SourceRange(SourceLocation(1, 5), SourceLocation(1, 8)))

    assert str(scope) == '[{line: 1, column: 1}, {line: 1, column: 8}]'
    assert len(scope) == 1


def test_multiline():
    scope = Scope(SourceRange(SourceLocation(1, 1), SourceLocation(1, 3)),
                  SourceRange(SourceLocation(4, 1), SourceLocation(4, 4)))

    assert str(scope) == '[{line: 1, column: 1}, {line: 4, column: 4}]'
    assert len(scope) == 4
