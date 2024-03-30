from codelimit.common.gsm.Automata import Automata
from codelimit.common.gsm.State import State


def state_to_dot(nfa: Automata, state: State, dot="", visited=None):
    if visited is None:
        visited = []
    if state in visited:
        return dot
    visited.append(state)
    if nfa.is_accepting(state):
        dot += f'{state.id} [label="{state.id}" peripheries=2]\n'
    else:
        dot += f'{state.id} [label="{state.id}"]\n'
    for transition in state.transition:
        target = transition[1]
        dot = state_to_dot(nfa, target, dot, visited)
    for target in state.epsilon_transitions:
        dot = state_to_dot(nfa, target, dot, visited)
    return dot


def state_transitions_to_dot(nfa: Automata, state: State, dot="", visited=None):
    if visited is None:
        visited = []
    if state in visited:
        return dot
    visited.append(state)
    for transition in state.transition:
        char = transition[0]
        target = transition[1]
        dot += f'{state.id} -> {target.id} [label="{char}"]\n'
        dot = state_transitions_to_dot(nfa, target, dot, visited)
    for target in state.epsilon_transitions:
        dot += f'{state.id} -> {target.id} [label="ε"]\n'
        dot = state_transitions_to_dot(nfa, target, dot, visited)
    return dot


def to_dot(nfa: Automata):
    result = "digraph {\n"
    result += 'rankdir="LR"\n'
    result += 'start [label = "start", style = "invis"]\n'
    result += state_to_dot(nfa, nfa.start)
    result += f'start -> {nfa.start.id} [label = "start"]\n'
    result += state_transitions_to_dot(nfa, nfa.start)
    result += "}"
    return result
