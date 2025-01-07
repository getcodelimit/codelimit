from dataclasses import dataclass

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange


@dataclass
class Header:
    name_token: Token
    token_range: TokenRange

    def name(self) -> str:
        return self.name_token.value


def sort_headers(headers: list[Header], tokens: list[Token], reverse=False) -> list[Header]:
    return sorted(
        headers,
        reverse=reverse,
        key=lambda h: (tokens[h.token_range.start].location.line, tokens[h.token_range.start].location.column),
    )
