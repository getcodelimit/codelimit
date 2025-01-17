from pygments.lexers import PythonLexer

from codelimit.common.lexer_utils import lex
from codelimit.languages import Languages
from codelimit.languages.Python import _get_indentation, _get_token_lines
from tests.conftest import assert_functions


def test_simple_function():
    code = """
    def foo():
        pass
    """

    assert_functions(code, Languages.Python, {"foo": 2})


def test_simple_function_larger_block():
    code = """
    def foo():
        foo = bar
        spam = eggs
    """

    assert_functions(code, Languages.Python, {"foo": 3})


def test_two_functions():
    code = """
    def foo():
        pass
    
    def bar():
        foo()
    """

    assert_functions(code, Languages.Python, {"foo": 2, "bar": 2})


def test_return_type():
    code = """
    def bar(
        bar: Bar
    ) -> JSONResponse:
        bar = foo
    """

    assert_functions(code, Languages.Python, {"bar": 4})


def test_two_functions_with_return_types():
    code = """
    def bar(
        bar: Bar
    ) -> JSONResponse:
        bar = foo
    
    def foo(
        foo: Foo
    ) -> None:
        foo = bar
    """

    assert_functions(code, Languages.Python, {"bar": 4, "foo": 4})


def test_get_indentation():
    assert _get_indentation("foo = True") == 0
    assert _get_indentation(" foo = True") == 1
    assert _get_indentation("    foo = True") == 4
    assert _get_indentation("\tfoo = True") == 4
    assert _get_indentation("\t \t foo = True") == 10
    assert _get_indentation("") is None
    assert _get_indentation("  ") is None
    assert _get_indentation("\t") is None


def test_no_functions():
    code = ""

    assert_functions(code, Languages.Python, {})


def test_trailing_global_code():
    code = """
    def foo():
        pass
    
    bar = [
        "bar"
    ]
    """

    assert_functions(code, Languages.Python, {"foo": 2})


def test_get_headers_multi_header_with_comment():
    code = """
    # def old_foo():
    def foo():
        pass
    
    def bar():
        foo()
    """

    assert_functions(code, Languages.Python, {"foo": 2, "bar": 2})


def test_do_not_count_comment_lines():
    code = """
    def foo():
    # This is a comment
        pass
        # This is also a comment
    """

    assert_functions(code, Languages.Python, {"foo": 2})


def test_header_with_defaults():
    code = """
    def foo(
        bar: str = SomeClass(
            'Hello'
        ),
        foo: str = SomeClass(
            'World'
        )
    ):
        pass
    """

    assert_functions(code, Languages.Python, {"foo": 9})


def test_header_type_hints():
    code = """
    def foo(
        bar: str
    ) -> FooBar:
        pass
    """

    assert_functions(code, Languages.Python, {"foo": 4})


def test_skip_function_with_nocl_comment_in_header():
    code = """
    def bar( # NOCL
        bar: Bar
    ) -> JSONResponse:
        bar = foo
    
    def foo(
        foo: Foo
    ) -> None:
        foo = bar
        bar = foo
    """

    assert_functions(code, Languages.Python, {"foo": 5})


def test_function_with_type_hints():
    code = """
    def foo(
        bar: Bar
    ) -> Foo:
        bar = foo
        foo = bar
    """

    assert_functions(code, Languages.Python, {"foo": 5})


def test_line_continuation():
    code = """
    def say_hello():
        print(\\
    "Hello " +\\
    "world")
    """

    assert_functions(code, Languages.Python, {"say_hello": 4})


def test_if_statement():
    code = """
    def foo():
        assert foo
        if bar:
            foo = bar
        else:
            bar = foo
    """

    assert_functions(code, Languages.Python, {"foo": 6})


def test_get_token_lines():
    code = ""
    code += "def foo():\n"
    code += "  pass\n"
    tokens = lex(PythonLexer(), code)

    result = _get_token_lines(tokens)

    assert len(result) == 2
    assert str(result[0]) == "[def, foo, (, ), :]"
    assert str(result[1]) == "[pass]"
