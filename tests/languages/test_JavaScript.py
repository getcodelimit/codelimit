from codelimit.languages import Language
from tests.common.ScopeExtractorTestCase import assert_units


def test_simple_function():
    code = """
    function foo() {
        return 'bar';
    }
    """

    assert_units(code, Language.JavaScript, {"foo": 3})
