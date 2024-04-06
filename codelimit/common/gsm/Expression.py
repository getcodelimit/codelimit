from typing import Iterable, TypeVar, TypeAlias

from codelimit.common.gsm.operator.Atom import Atom
from codelimit.common.gsm.operator.Concat import Concat
from codelimit.common.gsm.automata.DFA import DFA
from codelimit.common.gsm.automata.NFA import NFA
from codelimit.common.gsm.operator.Operator import Operator
from codelimit.common.gsm.predicate.Predicate import Predicate
from codelimit.common.gsm.automata.State import State

T = TypeVar("T")

Expression: TypeAlias = Operator | Predicate | T | list[Operator | Predicate | T]


def expression_to_nfa(expression: Expression[T]) -> NFA:
    if isinstance(expression, list):
        op_expression = [
            (item if isinstance(item, Operator) else Atom(item)) for item in expression
        ]
    else:
        op_expression = [
            (expression if isinstance(expression, Operator) else Atom(expression))
        ]
    nfa_stack: list[NFA] = []
    for item in op_expression:
        item.apply(nfa_stack)
        Concat().apply(nfa_stack)

    return nfa_stack.pop()


def epsilon_closure(states: State | Iterable[State]) -> set[State]:
    result = set()
    if isinstance(states, State):
        states = {states}
    for state in states:
        result.add(state)
        for s in state.epsilon_transitions:
            result.update(epsilon_closure(s))
    return result


def move(states: set[State], symbol: Predicate) -> set[State]:
    result = set()
    for state in states:
        for transition in state.transition:
            if transition[0] == symbol:
                result.add(transition[1])
    return result


def state_set_transitions(states: set[State]) -> set[Predicate]:
    result = set()
    for state in states:
        for transition in state.transition:
            result.add(transition[0])
    return result


def state_set_id(states: set[State]) -> str:
    return ", ".join([str(id) for id in sorted([state.id for state in states])])


def nfa_to_dfa(nfa: NFA) -> DFA:
    start = State()
    stack = [(start, epsilon_closure(nfa.start))]
    states: dict[str, State] = {}
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
        for predicate in transitions:
            new_states = epsilon_closure(move(T, predicate))
            if state_set_id(new_states) in states:
                new_state = states[state_set_id(new_states)]
            else:
                new_state = State()
                states[state_set_id(new_states)] = new_state
            state.transition.append((predicate, new_state))
            stack.append((new_state, new_states))
    return DFA(start, accepting_states)
