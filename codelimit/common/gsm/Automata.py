from codelimit.common.gsm.State import State


class Automata:
    def __init__(self, start: State, accepting: State | list[State]):
        self.start = start
        self.accepting = accepting

    def is_accepting(self, state: State) -> bool:
        if isinstance(self.accepting, list):
            return state in self.accepting
        else:
            return state == self.accepting

    def __str__(self):
        return f'Automata(start={self.start}, accepting={self.accepting})'