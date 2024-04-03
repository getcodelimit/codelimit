from codelimit.common.gsm.Expression import expression_to_nfa, Expression
from codelimit.common.gsm.automata.NFA import NFA
from codelimit.common.gsm.operator.Operator import Operator
from codelimit.common.gsm.automata.State import State


class Union(Operator):
    def __init__(self, left: Expression, right: Expression):
        self.left = left if isinstance(left, list) else [left]
        self.right = right if isinstance(right, list) else [right]

    def apply(self, stack: list[NFA]):
        start = State()
        nfa1 = expression_to_nfa(self.left)
        nfa2 = expression_to_nfa(self.right)
        start.epsilon_transitions = [nfa1.start, nfa2.start]
        accepting = State()
        nfa1.accepting.epsilon_transitions = [accepting]
        nfa2.accepting.epsilon_transitions = [accepting]
        stack.append(NFA(start, accepting))
