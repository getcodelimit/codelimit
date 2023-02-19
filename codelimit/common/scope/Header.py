from dataclasses import dataclass

from codelimit.common.TokenRange import TokenRange


@dataclass
class Header:
    name: str
    token_range: TokenRange
