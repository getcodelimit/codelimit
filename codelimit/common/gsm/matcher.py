import subprocess
import tempfile

from codelimit.common.gsm.Automata import Automata
from codelimit.common.gsm.Expression import expression_to_nfa, epsilon_closure
from codelimit.common.gsm.Operator import Operator
from codelimit.common.gsm.utils import to_dot


def match(expression: list[Operator | str], text: list):
    nfa = expression_to_nfa(expression)
    active_states = epsilon_closure(nfa.start)
    next_states = set()
    for char in text:
        for active_state in active_states:
            if active_state.transition and char == active_state.transition[0]:
                next_states.update(epsilon_closure(active_state.transition[1]))
        if not next_states:
            return False
        active_states = next_states
        next_states = set()
    return nfa.accepting in active_states


def render(expression: list[Operator | str]):
    render_nfa(expression_to_nfa(expression))


def render_nfa(nfa: Automata):
    dot = to_dot(nfa)
    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write(dot)
        f.flush()
        subprocess.run(['dot', '-Tpdf', f'-o{f.name}.pdf', f.name])
        subprocess.run(['open', f'{f.name}.pdf'])
