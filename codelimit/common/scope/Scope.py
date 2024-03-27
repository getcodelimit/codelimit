from __future__ import annotations

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header


class Scope:
    def __init__(self, header: Header, block: TokenRange):
        self.header = header
        self.block = block
        self.children: list[Scope] = []

    def __str__(self):
        return (
            f"[{self.header.token_range[0].location}, {self.block.tokens[-1].location}]"
        )

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return count_lines(self.tokens())

    def tokens(self):
        children_tokens = []
        for child in self.children:
            children_tokens.extend(child.tokens())
        return [
            t
            for t in self.header.token_range.tokens + self.block.tokens
            if t not in children_tokens
        ]

    def contains(self, other: Scope) -> bool:
        return self.header.token_range[0].location.lt(
            other.header.token_range[0].location
        ) and self.block.tokens[-1].location.gt(other.block.tokens[-1].location)


def count_lines(tokens: list[Token]):
    return len(set([t.location.line for t in tokens]))
