from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header


class Scope:
    def __init__(self, header: Header, block: TokenRange):
        self.header = header
        self.block = block

    def __str__(self):
        return (
            f"[{self.header.token_range[0].location}, {self.block.tokens[-1].location}]"
        )

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return count_lines(self.header.token_range.tokens + self.block.tokens)


def count_lines(tokens: list[Token]):
    return len(set([t.location.line for t in tokens]))
