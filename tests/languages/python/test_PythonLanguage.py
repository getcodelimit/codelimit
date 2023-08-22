from codelimit.languages.python.PythonLanguage import PythonLanguage


def test_accept_file():
    language = PythonLanguage()

    assert language.accept_file("foo.py")
    assert not language.accept_file("foo.js")
    assert not language.accept_file("test.c")
