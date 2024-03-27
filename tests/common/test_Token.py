from pygments.lexers import CLexer
from pygments.lexers import PythonLexer
from pygments.token import Keyword

from codelimit.common.Location import Location
from codelimit.common.Token import Token
from codelimit.common.lexer_utils import lex


def test_to_string():
    token = Token(Location(1, 1), Keyword, "def")

    assert str(token) == "def"


def test_is_token_type():
    tokens = lex(CLexer(), "int main(")

    assert tokens[0].is_keyword()
    assert tokens[1].is_name()
    assert tokens[2].is_symbol("(")


def test_keep_comment_token():
    code = ""
    code += "def foo(): # nocl\n"
    code += "  pass\n"

    tokens = lex(PythonLexer(), code, False)

    assert tokens[5].is_comment()


def test_equality():
    token1 = Token(Location(1, 1), Keyword, "def")
    token2 = Token(Location(1, 1), Keyword, "def")

    assert token1 == token2

    token3 = Token(Location(1, 2), Keyword, "def")
    token4 = Token(Location(1, 1), Keyword, "func")

    assert token1 != token3
    assert token1 != token4
