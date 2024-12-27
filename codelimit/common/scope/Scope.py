from __future__ import annotations

from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header


class Scope:
    def __init__(self, header: Header, block: TokenRange):
        self.header = header
        self.block = block
        self.children: list[Scope] = []

    def __str__(self):
        return f"({self.header.token_range.start}, {self.block.end})"

    def __repr__(self):
        return self.__str__()

    def contains(self, other: Scope) -> bool:
        return self.header.token_range.start < other.header.token_range.start and self.block.end > other.block.end
