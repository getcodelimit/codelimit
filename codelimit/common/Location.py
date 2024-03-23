from __future__ import annotations


class Location:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __str__(self):
        return f"{{line: {self.line}, column: {self.column}}}"

    def __repr__(self):
        return self.__str__()

    def lt(self, other: Location):
        return self.line < other.line or (
            self.line == other.line and self.column < other.column
        )

    def le(self, other: Location):
        return self.line < other.line or (
            self.line == other.line and self.column <= other.column
        )

    def gt(self, other: Location):
        return self.line > other.line or (
            self.line == other.line and self.column > other.column
        )

    def ge(self, other: Location):
        return self.line > other.line or (
            self.line == other.line and self.column >= other.column
        )

    def __eq__(self, other):
        if not isinstance(other, Location):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.line == other.line and self.column == other.column
