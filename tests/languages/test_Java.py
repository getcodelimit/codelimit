from codelimit.languages import Language
from tests.common.ScopeExtractorTestCase import assert_units


def test_simple_main_function():
    code = """
        public class T {
            public static void main(String[] args) {
                System.out.println("Hello world!");
            }
        }
    """

    assert_units(code, Language.Java, {"main": 3})


def test_two_functions():
    code = """
        public class T {
            private int one() {
                return 1;
            }
            private int two() {
                return 2;
            }
        }
    """

    assert_units(code, Language.Java, {"one": 3, 'two': 3})
