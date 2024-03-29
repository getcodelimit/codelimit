from codelimit.common.gsm.Automata import Automata
from codelimit.common.gsm.Operator import Operator
from codelimit.common.gsm.State import State


class Atom(Operator):
    def __init__(self, item: str):
        self.item = item

    def apply(self, stack: list[Automata]):
        start = State()
        accepting = State()
        start.transition = (self.item, accepting)
        stack.append(Automata(start, accepting))
