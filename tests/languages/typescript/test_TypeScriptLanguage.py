from codelimit.languages.typescript.TypeScriptLanguage import TypeScriptLanguage


def test_accept_file():
    language = TypeScriptLanguage()

    assert language.accept_file("main.ts")
    assert not language.accept_file("main.js")
