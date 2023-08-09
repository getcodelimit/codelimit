from codelimit.languages.typescript.TypeScriptLanguage import TypeScriptLanguage


def test_accept_file():
    language = TypeScriptLanguage()

    assert language.accept_file("main.ts")
    assert not language.accept_file("tests/main.ts")
    assert not language.accept_file("node_modules/main.ts")
