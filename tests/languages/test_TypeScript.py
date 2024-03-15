from codelimit.languages import LanguageName
from tests.common.ScopeExtractorTestCase import assert_units


def test_simple_function():
    code = """
    function foo(s: string): string {
        return `${s}bar`;
    }
    """

    assert_units(code, LanguageName.TypeScript, {"foo": 3})
