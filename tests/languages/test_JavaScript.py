from codelimit.languages import LanguageName
from tests.conftest import assert_units


def test_simple_function():
    code = """
    function foo() {
        return 'bar';
    }
    """

    assert_units(code, LanguageName.JavaScript, {"foo": 3})


def test_nested_functions():
    code = """
    function sayHelloWorld() {
        function sayHello() {
            console.log('Hello');
        }
        function sayWorld() {
            console.log('World');
        }
        sayHello();
        sayWorld();
    }

    sayHelloWorld();
    """

    assert_units(
        code,
        LanguageName.JavaScript,
        {"sayHelloWorld": 4, "sayHello": 3, "sayWorld": 3},
    )
