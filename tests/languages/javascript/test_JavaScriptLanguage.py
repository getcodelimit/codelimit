from codelimit.languages.javascript.JavaScriptLanguage import JavaScriptLanguage


def test_accept_file():
    language = JavaScriptLanguage()

    assert language.accept_file("main.js")
    assert not language.accept_file("tests/main.js")
    assert not language.accept_file("venv/main.js")
    assert not language.accept_file("node_modules/main.js")
