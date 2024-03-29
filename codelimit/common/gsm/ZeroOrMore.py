from codelimit.common.gsm.Expression import expression_to_nfa
from codelimit.common.gsm.Automata import Automata
from codelimit.common.gsm.Operator import Operator
from codelimit.common.gsm.State import State


class ZeroOrMore(Operator):
    def __init__(self, expression: Operator | str | list[Operator | str]):
        self.expression = expression if isinstance(expression, list) else [expression]

    def apply(self, stack: list[Automata]):
        start = State()
        nfa = expression_to_nfa(self.expression)
        accepting = State()
        start.epsilon_transitions = [nfa.start, accepting]
        nfa.accepting.epsilon_transitions = [nfa.start, accepting]
        stack.append(Automata(start, accepting))
