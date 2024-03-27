from codelimit.languages import LanguageName
from tests.conftest import assert_units


def test_simple_function():
    code = """
    function foo(s: string): string {
        return `${s}bar`;
    }
    """

    assert_units(code, LanguageName.TypeScript, {"foo": 3})


def test_arrow_function():
    code = """
    const sayHello = async () => {
        console.log('Hello world!');
    }
    """

    assert_units(code, LanguageName.TypeScript, {"sayHello": 3})


def test_nested_functions():
    code = """
    function Outer() {
        const sayHello = async () => {
            console.log('Hello world!');
        }
    
        sayHello();
    }
    """

    assert_units(code, LanguageName.TypeScript, {"Outer": 3, "sayHello": 3})
