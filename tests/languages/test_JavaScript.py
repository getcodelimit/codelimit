from codelimit.languages import Languages
from tests.conftest import assert_functions


def test_simple_function():
    code = """
    function foo() {
        return 'bar';
    }
    """

    assert_functions(code, Languages.JavaScript, {"foo": 3})


def test_arrow_function():
    code = """
    const sayHello = async () => {
        console.log('Hello world!');
    }
    """

    assert_functions(code, Languages.JavaScript, {"sayHello": 3})


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

    assert_functions(
        code,
        Languages.JavaScript,
        {"sayHelloWorld": 4, "sayHello": 3, "sayWorld": 3},
    )


def test_top_level_anonymous_functions_are_skipped():
    code = """
    function sayHelloWorld() {
        console.log('Hello World');
    }

    foo.on('sayHelloWorld', function () {
        console.log('Hello World');
    });
    """

    assert_functions(code, Languages.JavaScript, {"sayHelloWorld": 3})


def test_nested_anonymous_functions_are_skipped():
    code = """
    const say = () => {
        function helloWorld() {
            console.log('Hello World');
        }

        foo.on('helloWorld', function () {
            console.log('Hello World');
        });
    }
    """

    assert_functions(code, Languages.JavaScript, {"say": 5, "helloWorld": 3})


def test_nested_in_anonymous_function():
    code = """
    return this.each(function() {
        function stopQueue( elem, data, index ) {
            var hooks = data[ index ];
            jQuery.removeData( elem, index, true );
            hooks.stop( gotoEnd );
        }
    });
    """

    assert_functions(code, Languages.JavaScript, {"stopQueue": 5})
