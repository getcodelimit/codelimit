from codelimit.common.gsm.NFA import NFA
from codelimit.common.gsm.State import State


def state_to_dot(state: State, dot="", visited=None):
    if visited is None:
        visited = []
    if state in visited:
        return dot
    visited.append(state)
    if state.is_accepting():
        dot += f'{state.id} [label="{state.id}" peripheries=2]\n'
    else:
        dot += f'{state.id} [label="{state.id}"]\n'
    if state.transition:
        char = state.transition[0]
        target = state.transition[1]
        dot = state_to_dot(target, dot, visited)
        dot += f'{state.id} -> {target.id} [label="{char}"]\n'
    if state.epsilon_transitions:
        for target in state.epsilon_transitions:
            dot = state_to_dot(target, dot, visited)
            dot += f'{state.id} -> {target.id} [label="ε"]\n'
    return dot


def to_dot(nfa: NFA):
    result = "digraph {\n"
    result += 'rankdir="LR"\n'
    result += 'start [label = "start", style = "invis"]\n'
    result += state_to_dot(nfa.start)
    result += f'start -> {nfa.start.id} [label = "start"]\n'
    result += "}"
    return result
