from codelimit.common.TokenRange import TokenRange
from codelimit.languages.python.PythonLaguage import PythonLanguage


def test_str():
    tokens = PythonLanguage().lex('print("hello world"')
    block = TokenRange(tokens)

    assert str(block) == '[{line: 1, column: 1}, {line: 1, column: 19}]'
