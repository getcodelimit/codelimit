from __future__ import annotations

from codelimit.common.Token import Token


class TokenRange:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

    def __str__(self):
        return f"[{self.tokens[0].location}, {self.tokens[-1].location}]"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.tokens.__getitem__(item)

    def token_string(self):
        return " ".join([t.value for t in self.tokens])

    def lt(self, other: TokenRange):
        return self.tokens[-1].location.lt(other.tokens[0].location)

    def gt(self, other: TokenRange):
        return other.lt(self)

    def contains(self, other: TokenRange):
        return self.tokens[0].location.lt(other.tokens[0].location) and self.tokens[
            -1
        ].location.gt(other.tokens[-1].location)

    def overlaps(self, other: TokenRange):
        start_overlap = self.tokens[0].location.le(
            other.tokens[0].location
        ) and self.tokens[-1].location.ge(other.tokens[0].location)
        end_overlap = self.tokens[0].location.le(
            other.tokens[0].location
        ) and self.tokens[-1].location.ge(other.tokens[0].location)
        return start_overlap or end_overlap
