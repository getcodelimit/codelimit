import copy
from typing import TypeVar

from codelimit.common.gsm.Expression import (
    expression_to_nfa,
    epsilon_closure,
    nfa_to_dfa, Expression,
)
from codelimit.common.gsm.operator.Operator import Operator
from codelimit.common.gsm.Pattern import Pattern
from codelimit.common.gsm.utils import render_automata

T = TypeVar("T")


def match(expression: Expression, sequence: list) -> Pattern | None:
    nfa = expression_to_nfa(expression)
    dfa = nfa_to_dfa(nfa)
    pattern = Pattern(0, dfa)
    for item in sequence:
        next_state = None
        for transition in pattern.state.transition:
            if transition[0].accept(item):
                pattern.tokens.append(item)
                next_state = transition[1]
        if not next_state:
            return None
        else:
            pattern.state = next_state
    if pattern.state in dfa.accepting:
        return pattern
    else:
        return None


def starts_with(expression: Expression, sequence: list) -> Pattern | None:
    nfa = expression_to_nfa(expression)
    dfa = nfa_to_dfa(nfa)
    pattern = Pattern(0, dfa)
    for idx, item in enumerate(sequence):
        next_state = None
        for transition in pattern.state.transition:
            if transition[0].accept(item):
                pattern.tokens.append(item)
                next_state = transition[1]
        if not next_state:
            break
        else:
            pattern.state = next_state
    if pattern.state in dfa.accepting:
        pattern.end = len(pattern.tokens)
        return pattern
    else:
        return None


def find_all(expression: Expression, sequence: list) -> list[Pattern]:
    nfa = expression_to_nfa(expression)
    dfa = nfa_to_dfa(nfa)
    matches = []
    active_patterns = []
    last_match_idx = -1
    for idx, item in enumerate(sequence):
        dfa_copy = copy.deepcopy(dfa)
        active_patterns.append(Pattern(idx, dfa_copy))
        next_state_patterns = []
        for pattern in active_patterns:
            if pattern.start < last_match_idx:
                continue
            if len(pattern.state.transition) == 0 and pattern.is_accepting():
                pattern.end = idx
                matches.append(pattern)
                last_match_idx = idx
                continue
            for transition in pattern.state.transition:
                if transition[0].accept(item):
                    pattern.tokens.append(item)
                    pattern.state = transition[1]
                    next_state_patterns.append(pattern)
                    break
            else:
                if pattern.is_accepting():
                    pattern.end = idx
                    matches.append(pattern)
                    last_match_idx = idx
        active_patterns = next_state_patterns
    for pattern in active_patterns:
        if pattern.is_accepting():
            pattern.end = len(sequence)
            matches.append(pattern)
    return matches


def nfa_match(expression: Expression, sequence: list):
    nfa = expression_to_nfa(expression)
    active_states = epsilon_closure(nfa.start)
    next_states = set()
    for item in sequence:
        for active_state in active_states:
            for transition in active_state.transition:
                if transition[0].accept(item):
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
