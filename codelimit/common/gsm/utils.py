import subprocess
import tempfile

from codelimit.common.gsm.automata.Automata import Automata
from codelimit.common.gsm.automata.State import State


def state_to_dot(automata: Automata, state: State, dot="", visited=None):
    if visited is None:
        visited = []
    if state in visited:
        return dot
    visited.append(state)
    if automata.is_accepting(state):
        dot += f'{state.id} [label="{state.id}" peripheries=2]\n'
    else:
        dot += f'{state.id} [label="{state.id}"]\n'
    for transition in state.transition:
        target = transition[1]
        dot = state_to_dot(automata, target, dot, visited)
    for target in state.epsilon_transitions:
        dot = state_to_dot(automata, target, dot, visited)
    return dot


def state_transitions_to_dot(automata: Automata, state: State, dot="", visited=None):
    if visited is None:
        visited = []
    if state in visited:
        return dot
    visited.append(state)
    for transition in state.transition:
        char = transition[0]
        target = transition[1]
        dot += f'{state.id} -> {target.id} [label="{char}"]\n'
        dot = state_transitions_to_dot(automata, target, dot, visited)
    for target in state.epsilon_transitions:
        dot += f'{state.id} -> {target.id} [label="ε"]\n'
        dot = state_transitions_to_dot(automata, target, dot, visited)
    return dot


def render_automata(automata: Automata):
    dot = to_dot(automata)
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write(dot)
        f.flush()
        subprocess.run(["dot", "-Tpdf", f"-o{f.name}.pdf", f.name])
        subprocess.run(["open", f"{f.name}.pdf"])


def to_dot(automata: Automata):
    result = "digraph {\n"
    result += 'rankdir="LR"\n'
    result += 'start [label = "start", style = "invis"]\n'
    result += state_to_dot(automata, automata.start)
    result += f'start -> {automata.start.id} [label = "start"]\n'
    result += state_transitions_to_dot(automata, automata.start)
    result += "}"
    return result
