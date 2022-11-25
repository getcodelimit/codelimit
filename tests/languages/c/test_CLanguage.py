from codelimit.languages.c.CLanguage import CLanguage


def test_accept_file():
    language = CLanguage()

    assert language.accept_file('test.c')
    assert language.accept_file('test.C')
    assert language.accept_file('test.h')
    assert language.accept_file('test.H')
