from typing import Iterable

from codelimit.common.gsm.Atom import Atom
from codelimit.common.gsm.Automata import Automata
from codelimit.common.gsm.Concat import Concat
from codelimit.common.gsm.Operator import Operator
from codelimit.common.gsm.State import State


def expression_to_nfa(expression: list[Operator | str]) -> Automata:
    op_expression = [Atom(item) if isinstance(item, str) else item for item in expression]
    nfa_stack = []
    for item in op_expression:
        item.apply(nfa_stack)
        Concat().apply(nfa_stack)

    return nfa_stack.pop()


def epsilon_closure(states: State | Iterable[State]) -> set[State]:
    result = set()
    if isinstance(states, State):
        states: set[State] = {states}
    for state in states:
        result.add(state)
        if state.epsilon_transitions:
            for s in state.epsilon_transitions:
                result.update(epsilon_closure(s))
    return result


def move(states: set[State], symbol: str) -> set[State]:
    result = set()
    for state in states:
        if state.transition and state.transition[0] == symbol:
            result.add(state.transition[1])
    return result


def state_set_transitions(states: set[State]) -> set[str]:
    result = set()
    for state in states:
        if state.transition:
            result.add(state.transition[0])
    return result


def state_set_id(states: set[State]) -> str:
    return ", ".join([str(id) for id in sorted([state.id for state in states])])


def nfa_to_dfa(nfa: Automata) -> Automata:
    start = State()
    stack = [(start, epsilon_closure(nfa.start))]
    states = {}
    accepting_states = []
    marked_states = set()
    while stack:
        state, T = stack.pop()
        T_id = state_set_id(T)
        if T_id in marked_states:
            continue
        else:
            marked_states.add(T_id)
        if nfa.accepting in T:
            accepting_states.append(state)
        transitions = state_set_transitions(T)
        for atom in transitions:
            new_states = epsilon_closure(move(T, atom))
            if state_set_id(new_states) in states:
                new_state = states[state_set_id(new_states)]
            else:
                new_state = State()
                states[state_set_id(new_states)] = new_state
            if state.transition is None:
                state.transition = []
            state.transition.append((atom, new_state))
            stack.append((new_state, new_states))
    return Automata(start, accepting_states)
