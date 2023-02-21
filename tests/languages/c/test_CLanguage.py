from codelimit.languages.c.CLanguage import CLanguage


def test_accept_file():
    language = CLanguage()

    assert language.accept_file('main.c')
    assert language.accept_file('main.C')
    assert language.accept_file('main.h')
    assert language.accept_file('main.H')
