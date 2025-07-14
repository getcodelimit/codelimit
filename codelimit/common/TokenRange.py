from __future__ import annotations

from codelimit.common.Token import Token


class TokenRange:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __str__(self):
        return f"({self.start}, {self.end})"

    def __repr__(self):
        return self.__str__()

    def lt(self, other: TokenRange):
        return self.start < other.start

    def gt(self, other: TokenRange):
        return other.lt(self)

    def contains(self, other: TokenRange):
        return self.start < other.start and self.end > other.end

    def overlaps(self, other: TokenRange):
        start_overlap = self.start <= other.start <= self.end
        end_overlap = self.start <= other.end <= self.end
        return start_overlap or end_overlap


def sort_token_ranges(token_ranges: list[TokenRange], tokens: list[Token], reverse=False) -> list[TokenRange]:
    return sorted(
        token_ranges,
        reverse=reverse,
        key=lambda tr: (tokens[tr.start].location.line, tokens[tr.start].location.column),
    )
