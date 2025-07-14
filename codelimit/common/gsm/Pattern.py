from copy import deepcopy

from codelimit.common.TokenRange import TokenRange
from codelimit.common.gsm.automata.DFA import DFA
from codelimit.common.gsm.automata.State import State
from codelimit.common.gsm.predicate.Predicate import Predicate
from codelimit.common.token_matching.predicate.Balanced import Balanced


class Pattern(TokenRange):
    def __init__(self, automata: DFA, start: int = 0):
        super().__init__(start, start)
        self.automata = automata
        self.state = automata.start
        self.tokens: list = []
        self.predicate_map: dict[int, Predicate] = {}

    def consume(self, item) -> State | None:
        found_transition = False
        for transition in self.state.transition:
            predicate_id = id(transition[0])
            if predicate_id not in self.predicate_map:
                self.predicate_map[predicate_id] = deepcopy(transition[0])
            predicate = self.predicate_map[predicate_id]
            if predicate.accept(item):
                if found_transition:
                    raise ValueError("Multiple transitions found!")
                found_transition = True
                self.tokens.append(item)
                self.state = transition[1]
        return self.state if found_transition else None

    def is_accepting(self):
        for p in self.predicate_map.values():
            if isinstance(p, Balanced) and not p.depth == 0:
                return False
        return self.automata.is_accepting(self.state)

    def token_string(self):
        return " ".join([t.value for t in self.tokens])

    def __str__(self):
        return f'Pattern(start={self.start}, end={self.end}, tokens=[{self.token_string()}])'
