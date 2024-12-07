from copy import deepcopy

from codelimit.common.gsm.automata.DFA import DFA
from codelimit.common.gsm.automata.State import State
from codelimit.common.gsm.predicate.Predicate import Predicate


class Pattern:
    def __init__(self, start: int, automata: DFA):
        self.start = start
        self.end = start
        self.automata = automata
        self.state = automata.start
        self.tokens: list = []
        self.predicate_map: dict[int, Predicate] = {}

    def consume(self, item) -> State | None:
        for transition in self.state.transition:
            predicate_id = id(transition[0])
            if predicate_id not in self.predicate_map:
                self.predicate_map[predicate_id] = deepcopy(transition[0])
            predicate = self.predicate_map[predicate_id]
            if predicate.accept(item):
                self.tokens.append(item)
                self.state = transition[1]
                return self.state
        return None

    def is_accepting(self):
        return self.automata.is_accepting(self.state)

    def token_string(self):
        return " ".join([t.value for t in self.tokens])
