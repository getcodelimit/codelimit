from  codelimit.common.gsm.Automata import Automata
from  codelimit.common.gsm.Operator import Operator


class Concat(Operator):
    def apply(self, stack: list[Automata]):
        if len(stack) < 2:
            return
        nfa1 = stack.pop()
        nfa2 = stack.pop()
        nfa2.accepting.assign(nfa1.start)
        nfa = Automata(nfa2.start, nfa1.accepting)
        stack.append(nfa)
