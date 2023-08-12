from abc import ABC, abstractmethod
from typing import Union

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange


class TokenPredicate(ABC):
    def __init__(self):
        self.satisfied = False

    def reset(self):
        self.satisfied = False

    @abstractmethod
    def accept(self, token: Token) -> bool:
        pass


class KeywordPredicate(TokenPredicate):
    def __init__(self, keyword: str):
        super().__init__()
        self.keyword = keyword

    def accept(self, token: Token) -> bool:
        if token.is_keyword() and token.value == self.keyword:
            self.satisfied = True
            return True
        return False


class NamePredicate(TokenPredicate):
    def accept(self, token: Token) -> bool:
        if token.is_name():
            self.satisfied = True
            return True
        return False


class SymbolPredicate(TokenPredicate):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def accept(self, token: Token) -> bool:
        if token.is_symbol(self.symbol):
            self.satisfied = True
            return True
        return False


def match(
    tokens: list[Token], pattern: Union[TokenPredicate, list[TokenPredicate]]
) -> list[TokenRange]:
    result = []
    if not isinstance(pattern, list):
        pattern = [pattern]
    [p.reset() for p in pattern]
    pattern_index = 0
    match_index = -1
    for token_index in range(len(tokens)):
        token = tokens[token_index]
        predicate = pattern[pattern_index]
        if predicate.accept(token):
            if match_index < 0:
                match_index = token_index
            if predicate.satisfied:
                if pattern_index < len(pattern) - 1:
                    pattern_index += 1
                else:
                    result.append(TokenRange(tokens[match_index : token_index + 1]))
                    [p.reset() for p in pattern]
                    pattern_index = 0
                    match_index = -1
        else:
            [p.reset() for p in pattern]
            pattern_index = 0
            match_index = -1
    return result
