from abc import abstractmethod, ABC

from codelimit.common.gsm.automata.State import State


class Automata(ABC):
    def __init__(self, start: State):
        self.start = start

    @abstractmethod
    def is_accepting(self, state: State) -> bool:
        pass
