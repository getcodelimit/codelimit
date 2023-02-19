from codelimit.languages.python.PythonLaguage import PythonLanguage


def test_accept_file():
    language = PythonLanguage()

    assert language.accept_file('test.py')
    assert not language.accept_file('test.c')
    assert not language.accept_file('docs/venv/test.py')
