from pygments.lexers import PythonLexer
from pygments.lexers import CppLexer

from codelimit.common.Location import Location
from codelimit.common.lexer_utils import lex
from codelimit.common.source_utils import (
    index_to_location,
    location_to_index,
    get_newline_indices,
    get_location_range,
    filter_nocl_comment_tokens,
)


def test_index_to_location_single_line():
    code = "foo = bar"

    result = index_to_location(code, 5)

    assert result.line == 1
    assert result.column == 6


def test_index_to_location_multiline():
    code = ""
    code += "foo = bar\n"
    code += "spam = eggs\n"

    result = index_to_location(code, 16)

    assert result.line == 2
    assert result.column == 7


def test_index_to_location_index_is_newline():
    code = ""
    code += "foo = bar\n"
    code += "\n"

    result = index_to_location(code, 10)

    assert result.line == 2
    assert result.column == 0


def test_location_to_index():
    code = "foo = bar"

    result = location_to_index(code, Location(1, 5))

    assert result == 4


def test_location_to_index_multiline():
    code = ""
    code += "foo = bar\n"
    code += "spam = eggs\n"

    result = location_to_index(code, Location(2, 6))

    assert result == 15


def test_location_to_index_location_is_newline():
    code = ""
    code += "foo = bar\n"
    code += "\n"

    result = location_to_index(code, Location(2, 0))

    assert result == 10


def test_get_newline_indices():
    assert get_newline_indices("") == []
    assert get_newline_indices("\n") == [0]
    assert get_newline_indices(" \n \n") == [1, 3]
    assert get_newline_indices(" \n \n\nabcdef\n") == [1, 3, 4, 11]


def test_get_location_range():
    code = ""
    code += "def foo():\n"
    code += "  pass\n"
    code += "\n"
    code += "def bar():\n"
    code += "  i = 123\n"
    code += "  return i\n"
    code += "\n"

    result = get_location_range(code, Location(4, 1), Location(6, 12))

    expe = ""
    expe += "def bar():\n"
    expe += "  i = 123\n"
    expe += "  return i\n"

    assert result == expe


def test_filter_nocl_comments():
    code = ""
    code += "def foo():\n"
    code += "  pass\n"
    tokens = lex(PythonLexer(), code, False)

    result = filter_nocl_comment_tokens(tokens)

    assert len(result) == 0

    code = ""
    code += "def foo(): # nocl\n"
    code += "  pass\n"
    tokens = lex(PythonLexer(), code, False)

    result = filter_nocl_comment_tokens(tokens)

    assert len(result) == 1
    assert result[0].location.line == 1

    code = ""
    code += "// nocl\n"
    code += "void\n"
    code += "foo(Bar bar) {\n"
    code += "  bar.foo();\n"
    code += "}\n"
    tokens = lex(CppLexer(), code, False)

    result = filter_nocl_comment_tokens(tokens)

    assert len(result) == 1
    assert result[0].location.line == 1
