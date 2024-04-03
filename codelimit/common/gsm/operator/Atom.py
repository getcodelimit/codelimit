from typing import Any

from codelimit.common.gsm.predicate.Identity import Identity
from codelimit.common.gsm.automata.NFA import NFA
from codelimit.common.gsm.operator.Operator import Operator
from codelimit.common.gsm.predicate.Predicate import Predicate
from codelimit.common.gsm.automata.State import State


class Atom(Operator):
    def __init__(self, item: Any):
        self.item = item

    def apply(self, stack: list[NFA]):
        start = State()
        accepting = State()
        if isinstance(self.item, Predicate):
            start.transition.append((self.item, accepting))
        else:
            start.transition.append((Identity(self.item), accepting))
        stack.append(NFA(start, accepting))
