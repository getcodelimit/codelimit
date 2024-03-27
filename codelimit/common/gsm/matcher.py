import subprocess
import tempfile

from codelimit.common.gsm.Expression import expression_to_nfa
from codelimit.common.gsm.Operator import Operator
from codelimit.common.gsm.State import State
from codelimit.common.gsm.utils import to_dot


def _follow_epsilon_transitions(state: State) -> set[State]:
    result = {state}
    if state.epsilon_transitions:
        for s in state.epsilon_transitions:
            result.update(_follow_epsilon_transitions(s))
    return result


def match(expression: list[Operator | str], text: list):
    nfa = expression_to_nfa(expression)
    active_states = _follow_epsilon_transitions(nfa.start)
    next_states = set()
    for char in text:
        for active_state in active_states:
            if active_state.transition and char == active_state.transition[0]:
                next_states.update(_follow_epsilon_transitions(active_state.transition[1]))
        if not next_states:
            return False
        active_states = next_states
        next_states = set()
    return nfa.accepting in active_states


def render(expression: list[Operator | str]):
    nfa = expression_to_nfa(expression)
    dot = to_dot(nfa)
    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write(dot)
        f.flush()
        subprocess.run(['dot', '-Tpdf', f'-o{f.name}.pdf', f.name])
        subprocess.run(['open', f'{f.name}.pdf'])
