from copy import deepcopy

from codelimit.common.gsm.automata.DFA import DFA
from codelimit.common.gsm.automata.State import State
from codelimit.common.gsm.predicate.Predicate import Predicate
from codelimit.common.token_matching.predicate.Balanced import Balanced
from codelimit.common.TokenRange import TokenRange


class Pattern(TokenRange):
    def __init__(self, automata: DFA, start: int = 0):
        super().__init__(start, start)
        self.automata = automata
        self.state = automata.start
        self.tokens: list = []
        self.predicate_map: dict[int, Predicate] = {}

    def consume(self, item) -> State | None:
        found_transition = False
        transitions = self._select_transitions(item)
        for transition in transitions:
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

    def _select_transitions(self, item) -> list[tuple[Predicate, State]]:
        result = []
        for transition in self.state.transition:
            predicate_id = id(transition[0])
            if predicate_id not in self.predicate_map:
                test_predicate = deepcopy(transition[0])
            else:
                test_predicate = deepcopy(self.predicate_map[predicate_id])
            if test_predicate.accept(item):
                result.append(transition)
        if len(result) <= 1:
            return result
        else:
            return [t for t in result if id(t[0]) in self.predicate_map]

    def is_accepting(self):
        for p in self.predicate_map.values():
            if isinstance(p, Balanced) and not p.depth == 0:
                return False
        return self.automata.is_accepting(self.state)

    def token_string(self):
        return " ".join([t.value for t in self.tokens])

    def __str__(self):
        return f"Pattern(start={self.start}, end={self.end}, tokens=[{self.token_string()}])"
