from typing import Union

from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.token_matching.predicates.Lookahead import Lookahead
from codelimit.common.token_matching.predicates.TokenPredicate import TokenPredicate


def match(
    tokens: list[Token], pattern: Union[TokenPredicate, list[TokenPredicate]]
) -> list[TokenRange]:
    result = []
    if not isinstance(pattern, list):
        pattern = [pattern]
    [p.reset() for p in pattern]
    pattern_index = 0
    match_index = -1
    matched_tokens = []
    for token_index in range(len(tokens)):
        token = tokens[token_index]
        predicate = pattern[pattern_index]
        if predicate.accept(token):
            if not isinstance(predicate, Lookahead):
                matched_tokens.append(token)
            if match_index < 0:
                match_index = token_index
            if predicate.satisfied:
                if pattern_index < len(pattern) - 1:
                    pattern_index += 1
                else:
                    result.append(TokenRange(matched_tokens))
                    [p.reset() for p in pattern]
                    pattern_index = 0
                    match_index = -1
                    matched_tokens = []
        else:
            [p.reset() for p in pattern]
            pattern_index = 0
            match_index = -1
            matched_tokens = []
    return result
