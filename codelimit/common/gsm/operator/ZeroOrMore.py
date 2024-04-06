from codelimit.common.gsm.Expression import expression_to_nfa, Expression
from codelimit.common.gsm.automata.NFA import NFA
from codelimit.common.gsm.operator.Operator import Operator
from codelimit.common.gsm.automata.State import State


class ZeroOrMore(Operator):
    def __init__(self, expression: Expression):
        self.expression = expression if isinstance(expression, list) else [expression]

    def apply(self, stack: list[NFA]):
        start = State()
        nfa = expression_to_nfa(self.expression)
        accepting = State()
        start.epsilon_transitions = [nfa.start, accepting]
        nfa.accepting.epsilon_transitions = [nfa.start, accepting]
        stack.append(NFA(start, accepting))
