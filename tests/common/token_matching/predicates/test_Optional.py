from pygments.lexers import PythonLexer

from codelimit.common.lexer_utils import lex
from codelimit.common.token_matching.predicates.Keyword import Keyword
from codelimit.common.token_matching.predicates.Optional import Optional


def test_optional():
    tokens = lex(PythonLexer(), "def foo(): pass")
    optional = Optional(Keyword("def"))

    assert optional.satisfied
    assert optional.accept(tokens[0])
    assert optional.satisfied
    assert not optional.accept(tokens[0])

    optional.reset()

    assert optional.satisfied
    assert optional.accept(tokens[0])