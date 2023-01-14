from __future__ import annotations


class SourceLocation:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __str__(self):
        return f'{{line: {self.line}, column: {self.column}}}'

    def __repr__(self):
        return self.__str__()

    def lt(self, other: SourceLocation):
        return self.line < other.line or (self.line == other.line and self.column < other.column)

    def le(self, other: SourceLocation):
        return self.line < other.line or (self.line == other.line and self.column <= other.column)

    def gt(self, other: SourceLocation):
        return self.line > other.line or (self.line == other.line and self.column > other.column)

    def ge(self, other: SourceLocation):
        return self.line > other.line or (self.line == other.line and self.column >= other.column)