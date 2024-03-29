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
    if state.transition:
        if isinstance(state.transition, list):
            for transition in state.transition:
                char = transition[0]
                target = transition[1]
                dot = state_to_dot(nfa, target, dot, visited)
                dot += f'{state.id} -> {target.id} [label="{char}"]\n'
        else:
            char = state.transition[0]
            target = state.transition[1]
            dot = state_to_dot(nfa, target, dot, visited)
            dot += f'{state.id} -> {target.id} [label="{char}"]\n'
    for target in state.epsilon_transitions:
        dot = state_to_dot(nfa, target, dot, visited)
        dot += f'{state.id} -> {target.id} [label="ε"]\n'
    return dot


def state_transistions_to_dot(nfa: Automata, state: State, dot="", visited=None):
    if visited is None:
        visited = []
    if state in visited:
        return dot
    visited.append(state)
    if nfa.is_accepting(state):
        dot += f'{state.id} [label="{state.id}" peripheries=2]\n'
    else:
        dot += f'{state.id} [label="{state.id}"]\n'
    if state.transition:
        if isinstance(state.transition, list):
            for transition in state.transition:
                char = transition[0]
                target = transition[1]
                dot = state_to_dot(nfa, target, dot, visited)
                dot += f'{state.id} -> {target.id} [label="{char}"]\n'
        else:
            char = state.transition[0]
            target = state.transition[1]
            dot = state_to_dot(nfa, target, dot, visited)
            dot += f'{state.id} -> {target.id} [label="{char}"]\n'
    for target in state.epsilon_transitions:
        dot = state_to_dot(nfa, target, dot, visited)
        dot += f'{state.id} -> {target.id} [label="ε"]\n'
    return dot


def to_dot(nfa: Automata):
    result = "digraph {\n"
    result += 'rankdir="LR"\n'
    result += 'start [label = "start", style = "invis"]\n'
    result += state_to_dot(nfa, nfa.start)
    result += f'start -> {nfa.start.id} [label = "start"]\n'
    result += "}"
    return result
