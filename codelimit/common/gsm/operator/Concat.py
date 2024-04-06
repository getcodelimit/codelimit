from codelimit.common.gsm.automata.NFA import NFA
from codelimit.common.gsm.operator.Operator import Operator


class Concat(Operator):
    def apply(self, stack: list[NFA]):
        if len(stack) < 2:
            return
        nfa1 = stack.pop()
        nfa2 = stack.pop()
        nfa2.accepting.assign(nfa1.start)
        nfa = NFA(nfa2.start, nfa1.accepting)
        stack.append(nfa)
