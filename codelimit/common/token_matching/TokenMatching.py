from abc import ABC, abstractmethod
from typing import Union

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange


class TokenPredicate(ABC):

    @abstractmethod
    def accept(self, token: Token) -> bool:
        pass


class KeywordPredicate(TokenPredicate):
    def __init__(self, keyword: str):
        self.keyword = keyword

    def accept(self, token: Token) -> bool:
        return token.is_keyword() and token.value == self.keyword


class NamePredicate(TokenPredicate):

    def accept(self, token: Token) -> bool:
        return token.is_name()


def match(tokens: list[Token], pattern: Union[TokenPredicate, list[TokenPredicate]]) -> list[TokenRange]:
    result = []
    if not isinstance(pattern, list):
        pattern = [pattern]
    pattern_index = 0
    match_index = -1
    for token_index in range(len(tokens)):
        token = tokens[token_index]
        if pattern[pattern_index].accept(token):
            if match_index < 0:
                match_index = token_index
            if pattern_index < len(pattern) - 1:
                pattern_index += 1
            else:
                result.append(TokenRange(tokens[match_index:token_index + 1]))
        else:
            pattern_index = 0
            match_index = -1
    return result
