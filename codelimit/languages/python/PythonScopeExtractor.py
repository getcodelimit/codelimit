from codelimit.common.Token import Token
from codelimit.common.TokenRange import TokenRange
from codelimit.common.scope.Header import Header
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.token_matching.TokenMatching import match, KeywordPredicate, NamePredicate


class PythonScopeExtractor(ScopeExtractor):

    def extract_headers(self, tokens: list[Token]) -> list[Header]:
        result = []
        matches = match(tokens, [KeywordPredicate('def'), NamePredicate()])
        for m in matches:
            result.append(Header(m.tokens[1].value, m))
        return result

    def extract_blocks(self, tokens: list[Token]) -> list[TokenRange]:
        lines = _get_token_lines(tokens)
        result = []
        indentation = None
        scope_tokens = []
        for line in lines:
            token_indentation = line[0].location.column
            if len(scope_tokens) == 0:
                scope_tokens.extend(line)
                indentation = token_indentation
            else:
                if token_indentation == indentation:
                    scope_tokens.extend(line)
                else:
                    result.append(TokenRange(scope_tokens))
                    indentation = token_indentation
                    scope_tokens = line
        if len(scope_tokens) > 0:
            result.append(TokenRange(scope_tokens))
        return result


def _get_token_lines(tokens: list[Token]) -> list[list[Token]]:
    result = []
    line = []
    line_continuation = False
    line_nr = 0
    for t in tokens:
        if len(line) == 0:
            line.append(t)
            line_nr = t.location.line
        else:
            if line_continuation:
                line.append(t)
                line_nr = t.location.line
                line_continuation = False
            if t.location.line == line_nr:
                line.append(t)
                if t.value.endswith("\\\n"):
                    line_continuation = True
            else:
                result.append(line)
                line = [t]
                line_nr = t.location.line
    if len(line) > 0:
        result.append(line)
    return result


def _get_indentation(line: str):
    result = 0
    for c in line:
        if c == ' ':
            result += 1
        elif c == '\t':
            result += 4
        else:
            return result
    return None
