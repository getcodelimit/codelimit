from codelimit.common.gsm.Expression import expression_to_nfa
from codelimit.common.gsm.NFA import NFA
from codelimit.common.gsm.Operator import Operator
from codelimit.common.gsm.State import State


class OneOrMore(Operator):
    def __init__(self, expression: Operator | str | list[Operator | str]):
        self.expression = expression if isinstance(expression, list) else [expression]

    def apply(self, stack: list[NFA]):
        start = State()
        nfa = expression_to_nfa(self.expression)
        accepting = State()
        start.epsilon_transitions = [nfa.start]
        nfa.accepting.epsilon_transitions = [nfa.start, accepting]
        stack.append(NFA(start, accepting))
