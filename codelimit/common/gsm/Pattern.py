from codelimit.common.gsm.automata.Automata import Automata


class Pattern:
    def __init__(self, start: int, automata: Automata):
        self.start = start
        self.automata = automata
        self.state = automata.start
        self.tokens: list = []

    def is_accepting(self):
        return self.automata.is_accepting(self.state)
