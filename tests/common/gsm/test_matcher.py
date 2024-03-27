from codelimit.common.gsm import ZeroOrMore
from codelimit.common.gsm.OneOrMore import OneOrMore
from codelimit.common.gsm.Optional import Optional
from codelimit.common.gsm.Union import Union
from codelimit.common.gsm.ZeroOrMore import ZeroOrMore
from codelimit.common.gsm.matcher import match, render


def test_single_atom():
    assert match(['a'], ['a'])
    assert not match(['b'], ['a'])


def test_sequence():
    assert match(['a', 'b'], ['a', 'b'])
    assert not match(['a', 'b'], ['a', 'b', 'c'])


def test_union():
    assert match([Union('a', 'b')], ['a'])

    expr = ['a', Union('a', 'b')]
    text = ['a', 'a']

    assert match(expr, text)

    text = ['a', 'b']
    assert match(expr, text)

    expr = ['a', Union(Union('a', 'b'), 'c')]

    assert match(expr, ['a', 'a'])
    assert match(expr, ['a', 'b'])
    assert match(expr, ['a', 'c'])


def test_zero_or_more():
    expr = [ZeroOrMore(Union('a', 'b'))]

    assert match(expr, [])
    assert match(expr, ['a'])
    assert match(expr, ['a', 'a'])
    assert match(expr, ['b'])
    assert match(expr, ['b', 'b'])
    assert not match(expr, ['c'])
    assert not match(expr, ['a', 'c'])


def test_dragon_book_example():
    expr = [ZeroOrMore(Union('a', 'b')), 'a', 'b', 'b']

    assert match(expr, ['a', 'b', 'b'])


def test_one_or_more():
    expr = [OneOrMore(Union('a', 'b'))]

    assert not match(expr, [])
    assert match(expr, ['a'])
    assert match(expr, ['a', 'a'])
    assert match(expr, ['b'])
    assert match(expr, ['b', 'b'])
    assert not match(expr, ['c'])
    assert not match(expr, ['a', 'c'])


def test_optional():
    expr = ['a', Optional('b')]

    assert match(expr, ['a'])
    assert match(expr, ['a', 'b'])
    assert match([Optional('b')], [])
    assert match([Optional('b')], ['b'])
    assert not match([Optional('b')], ['b', 'b'])