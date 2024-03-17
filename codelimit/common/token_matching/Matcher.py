from typing import Union

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.token_matching.predicates.Lookahead import Lookahead
from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate


class Matcher:
    def __init__(self, pattern: Union[TokenPredicate, list[TokenPredicate]]):
        if not isinstance(pattern, list):
            self._pattern = [pattern]
        else:
            self._pattern = pattern
        self._matches: list[TokenRange] = []
        self._reset()

    def _reset(self):
        [p.reset() for p in self._pattern]
        self._pattern_index = 0
        self._matched_tokens = []

    def match(self, tokens: list[Token]) -> list[TokenRange]:
        [p.reset() for p in self._pattern]
        for token_index in range(len(tokens)):
            token = tokens[token_index]
            predicate = self._pattern[self._pattern_index]
            if predicate.accept(token):
                self._consume_token(token)
            else:
                self._reset()
                predicate = self._pattern[self._pattern_index]
                if predicate.accept(token):
                    self._consume_token(token)

        return self._matches

    def _consume_token(self, token: Token):
        predicate = self._pattern[self._pattern_index]
        if not isinstance(predicate, Lookahead):
            self._matched_tokens.append(token)
        if predicate.satisfied:
            if self._pattern_index < len(self._pattern) - 1:
                self._pattern_index += 1
            else:
                self._matches.append(TokenRange(self._matched_tokens))
                self._reset()