from textwrap import dedent

import pytest

from codelimit.common.gsm.Expression import expression_to_nfa, nfa_to_dfa
from codelimit.common.gsm.automata.State import State
from codelimit.common.gsm.matcher import match, nfa_match, find_all, starts_with
from codelimit.common.gsm.operator.OneOrMore import OneOrMore
from codelimit.common.gsm.operator.Optional import Optional
from codelimit.common.gsm.operator.Union import Union
from codelimit.common.gsm.operator.ZeroOrMore import ZeroOrMore
from codelimit.common.gsm.predicate.Predicate import Predicate
from codelimit.common.gsm.utils import to_dot


def test_single_atom():
    assert nfa_match(["a"], ["a"])
    assert not nfa_match(["b"], ["a"])

    assert match(["a"], ["a"])
    assert not match(["b"], ["a"])


def test_sequence():
    assert nfa_match(["a", "b"], ["a", "b"])
    assert not nfa_match(["a", "b"], ["a", "b", "c"])

    assert match(["a", "b"], ["a", "b"])
    assert not match(["a", "b"], ["a", "b", "c"])


def test_to_string():
    State._id = 1

    expr = ["a", "b"]
    nfa = expression_to_nfa(expr)

    assert str(nfa) == "NFA(start=State(1), accepting=State(4))"


def test_to_dot():
    State._id = 1
    expr = ["a", "b"]
    nfa = expression_to_nfa(expr)
    result = to_dot(nfa)

    expected = """
    digraph {
    rankdir="LR"
    start [label = "start", style = "invis"]
    1 [label="1"]
    3 [label="3"]
    4 [label="4" peripheries=2]
    start -> 1 [label = "start"]
    1 -> 3 [label="a"]
    3 -> 4 [label="b"]
    }
    """

    assert result.strip() == dedent(expected).strip()


def test_union():
    assert nfa_match([Union("a", "b")], ["a"])
    assert match([Union("a", "b")], ["a"])

    expr = ["a", Union("a", "b")]
    text = ["a", "a"]

    assert match(expr, text)

    text = ["a", "b"]
    assert match(expr, text)

    expr = ["a", Union(Union("a", "b"), "c")]

    assert nfa_match(expr, ["a", "a"])
    assert match(expr, ["a", "a"])
    assert nfa_match(expr, ["a", "b"])
    assert match(expr, ["a", "b"])
    assert nfa_match(expr, ["a", "c"])
    assert match(expr, ["a", "c"])


def test_zero_or_more():
    expr = [ZeroOrMore(Union("a", "b"))]

    assert match(expr, [])
    assert match(expr, ["a"])
    assert match(expr, ["a", "a"])
    assert match(expr, ["b"])
    assert match(expr, ["b", "b"])
    assert not match(expr, ["c"])
    assert not match(expr, ["a", "c"])


def test_dragon_book_example():
    expr = [ZeroOrMore(Union("a", "b")), "a", "b", "b"]

    assert nfa_match(expr, ["a", "b", "b"])
    assert match(expr, ["a", "b", "b"])


def test_thesis_example():
    expr = [Optional("c"), OneOrMore("a")]

    assert match(expr, ["c", "a", "a"])


def test_one_or_more():
    expr = [OneOrMore(Union("a", "b"))]

    assert not match(expr, [])
    assert match(expr, ["a"])
    assert match(expr, ["a", "a"])
    assert match(expr, ["b"])
    assert match(expr, ["b", "b"])
    assert not match(expr, ["c"])
    assert not match(expr, ["a", "c"])


def test_optional():
    expr = ["a", Optional("b")]

    assert match(expr, ["a"])
    assert match(expr, ["a", "b"])
    assert match([Optional("b")], [])
    assert match([Optional("b")], ["b"])
    assert not match([Optional("b")], ["b", "b"])


def test_nfa_to_dfa():
    expr = [Union(OneOrMore("a"), OneOrMore("b"))]
    nfa = expression_to_nfa(expr)
    dfa = nfa_to_dfa(nfa)

    assert dfa is not None


def test_find_all():
    expr = [OneOrMore("a")]
    text = ["a", "a", "b", "b", "a", "b", "b"]

    matches = find_all(expr, text)

    assert len(matches) == 2
    assert matches[0].start == 0
    assert matches[0].end == 2
    assert matches[1].start == 4
    assert matches[1].end == 5


def test_find_all_nested_should_prioritize_longest_match():
    expr = [OneOrMore("a")]
    text = ["a", "a", "b", "b", "a", "b", "b", "a", "a"]

    matches = find_all(expr, text, nested=True)

    assert len(matches) == 3
    assert matches[0].start == 0
    assert matches[0].end == 2
    assert matches[1].start == 4
    assert matches[1].end == 5
    assert matches[2].start == 7
    assert matches[2].end == 9

def test_single_item():
    expr = ["a"]
    text = ["a", "a", "b", "a"]

    matches = find_all(expr, text)

    assert len(matches) == 3


class CharacterRange(Predicate[str]):
    def __init__(self, start: str, end: str):
        self.start = ord(start[0])
        self.end = ord(end[0])

    def accept(self, item: str) -> bool:
        return len(item) == 1 and self.start <= ord(item[0]) <= self.end

    def __str__(self):
        return f"[{chr(self.start)}{chr(self.end)}]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CharacterRange):
            return False
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))


def test_predicate():
    expr = CharacterRange("a", "c")
    text = ["a", "a", "b", "b", "x", "y", "c"]

    matches = find_all(expr, text)

    assert len(matches) == 5

    expr = [OneOrMore(CharacterRange("a", "c"))]

    matches = find_all(expr, text)

    assert len(matches) == 2


def test_starts_with():
    expr = [ZeroOrMore("a"), "b"]
    text = ["a", "a", "b", "b", "a", "b", "b"]

    pattern = starts_with(expr, text)

    assert pattern is not None
    assert pattern.start == 0
    assert pattern.end == 3

    text = ["a", "a", "b"]

    pattern = starts_with(expr, text)

    assert pattern is not None
    assert pattern.start == 0
    assert pattern.end == 3

    text = ["a", "a"]

    pattern = starts_with(expr, text)

    assert pattern is None


class Not(Predicate[str]):
    def __init__(self, value: str):
        self.value = value

    def accept(self, item: str) -> bool:
        return self.value != item

    def __str__(self):
        return f"[^{self.value}]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Not):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


def test_starts_with_overlapping_predicates():
    expr = [ZeroOrMore(Not("c")), "b"]
    text = ["a", "a", "b", "b"]

    with pytest.raises(ValueError):
        starts_with(expr, text)
