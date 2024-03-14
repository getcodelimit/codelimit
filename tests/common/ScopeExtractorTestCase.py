import unittest
from abc import abstractmethod
from textwrap import dedent

from pygments.lexers import get_lexer_by_name

from codelimit.common.lexer_utils import lex
from codelimit.common.scope.scope_extractor_utils import build_scopes
from codelimit.common.utils import load_scope_extractor_by_name
from codelimit.languages import Language


class ScopeExtractorTestCase(unittest.TestCase):
    @abstractmethod
    def test_extract_headers_single_header(self):
        pass

    @abstractmethod
    def test_extract_blocks_single_block(self):
        pass

    @abstractmethod
    def test_extract_blocks_multiple_blocks(self):
        pass

    @abstractmethod
    def test_single_scope(self):
        pass

    @abstractmethod
    def test_multiple_scopes(self):
        pass


def assert_units(code: str, language: Language, units: dict[str, int]):
    code = dedent(code).strip('\n')
    lexer = get_lexer_by_name(language.value)
    tokens = lex(lexer, code)
    scope_extractor = load_scope_extractor_by_name(language.value)
    if not scope_extractor:
        raise ValueError(f"Scope extractor not found for {language.value}")
    scopes = build_scopes(tokens, scope_extractor)
    assert len(scopes) == len(units)
    for idx, scope in enumerate(scopes):
        assert scope.header.name in units
        assert len(scope) == units[scope.header.name]
