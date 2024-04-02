import copy
from typing import TypeVar

from codelimit.common.gsm.Expression import expression_to_nfa, epsilon_closure, nfa_to_dfa
from codelimit.common.gsm.Operator import Operator
from codelimit.common.gsm.Pattern import Pattern
from codelimit.common.gsm.Predicate import Predicate
from codelimit.common.gsm.utils import render_automata

T = TypeVar('T')


def match(expression: Operator | Predicate[T] | T | list[Operator | Predicate[T] | T], text: list) -> Pattern | None:
    nfa = expression_to_nfa(expression)
    dfa = nfa_to_dfa(nfa)
    pattern = Pattern(0, dfa)
    for char in text:
        next_state = None
        for transition in pattern.state.transition:
            if transition[0] == char:
                pattern.tokens.append(char)
                next_state = transition[1]
        if not next_state:
            return None
        else:
            pattern.state = next_state
    if pattern.state in dfa.accepting:
        return pattern
    else:
        return None


def find_all(expression: list[Operator | str], text: list) -> list[Pattern]:
    nfa = expression_to_nfa(expression)
    dfa = nfa_to_dfa(nfa)
    matches = []
    active_patterns = []
    last_match_idx = -1
    for idx, char in enumerate(text):
        dfa_copy = copy.deepcopy(dfa)
        active_patterns.append(Pattern(idx, dfa_copy))
        next_state_patterns = []
        for pattern in active_patterns:
            if pattern.start <= last_match_idx:
                continue
            for transition in pattern.state.transition:
                if transition[0] == char:
                    pattern.tokens.append(char)
                    pattern.state = transition[1]
                    next_state_patterns.append(pattern)
                else:
                    if pattern.is_accepting():
                        matches.append(pattern)
                        last_match_idx = idx
        active_patterns = next_state_patterns
    return matches


def nfa_match(expression: list[Operator | str], text: list):
    nfa = expression_to_nfa(expression)
    active_states = epsilon_closure(nfa.start)
    next_states = set()
    for char in text:
        for active_state in active_states:
            for transition in active_state.transition:
                if transition[0] == char:
                    next_states.update(epsilon_closure(transition[1]))
        if not next_states:
            return False
        active_states = next_states
        next_states = set()
    return nfa.accepting in active_states


def render_nfa(expression: list[Operator | str]):
    render_automata(expression_to_nfa(expression))


def render_dfa(expression: list[Operator | str]):
    render_automata(nfa_to_dfa(expression_to_nfa(expression)))
