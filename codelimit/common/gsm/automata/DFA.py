from codelimit.common.gsm.automata.Automata import Automata
from codelimit.common.gsm.automata.State import State


class DFA(Automata):
    def __init__(self, start: State, accepting: list[State]):
        super().__init__(start)
        self.accepting = accepting

    def is_accepting(self, state: State) -> bool:
        return state in self.accepting

    def __str__(self):
        return f"DFA(start={self.start}, accepting={self.accepting})"
