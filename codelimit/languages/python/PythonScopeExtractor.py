from re import finditer

from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.SourceRange import SourceRange
from codelimit.common.source_utils import index_to_location
from codelimit.languages.ScopeExtractor import ScopeExtractor


class PythonScopeExtractor(ScopeExtractor):

    def extract_headers(self, code: str) -> list[SourceRange]:
        result = []
        for match in finditer(r'\b(def)\b', code):
            start_index = match.span(1)[0]
            end_index = match.span(1)[1]
            header = SourceRange(index_to_location(code, start_index), index_to_location(code, end_index - 1))
            result.append(header)
        return result

    def extract_blocks(self, code: str) -> list[SourceRange]:
        result = []
        lines = code.split('\n')
        line_nr = 0
        indentation = None
        start = None
        end = None
        for line in lines:
            line_nr += 1
            line_indentation = _get_indentation(line)
            if line_indentation is None:
                continue
            if start is None:
                start = SourceLocation(line_nr, line_indentation + 1)
            elif line_indentation != indentation:
                result.append(SourceRange(start, end))
                start = SourceLocation(line_nr, line_indentation + 1)
            end = SourceLocation(line_nr, len(line))
            indentation = line_indentation
        if start and indentation is not None:
            result.append(SourceRange(start, end))
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
