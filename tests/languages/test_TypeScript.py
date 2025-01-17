from codelimit.languages import Languages
from tests.conftest import assert_functions


def test_simple_function():
    code = """
    function foo(s: string): string {
        return `${s}bar`;
    }
    """

    assert_functions(code, Languages.TypeScript, {"foo": 3})


def test_arrow_function():
    code = """
    const sayHello = async () => {
        console.log('Hello world!');
    }
    """

    assert_functions(code, Languages.TypeScript, {"sayHello": 3})


def test_nested_functions():
    code = """
    function Outer() {
        const sayHello = async () => {
            console.log('Hello world!');
        }
    
        sayHello();
    }
    """

    assert_functions(code, Languages.TypeScript, {"Outer": 3, "sayHello": 3})
