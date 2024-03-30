import subprocess
import tempfile

from codelimit.common.gsm.Automata import Automata
from codelimit.common.gsm.Expression import expression_to_nfa, epsilon_closure, nfa_to_dfa
from codelimit.common.gsm.Operator import Operator
from codelimit.common.gsm.utils import to_dot


def match(expression: list[Operator | str], text: list):
    nfa = expression_to_nfa(expression)
    dfa = nfa_to_dfa(nfa)
    state = dfa.start
    for char in text:
        next_state = None
        for transition in state.transition:
            if transition[0] == char:
                next_state = transition[1]
        if not next_state:
            return False
        else:
            state = next_state
    return state in dfa.accepting


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


def render_automata(automata: Automata):
    dot = to_dot(automata)
    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write(dot)
        f.flush()
        subprocess.run(['dot', '-Tpdf', f'-o{f.name}.pdf', f.name])
        subprocess.run(['open', f'{f.name}.pdf'])
