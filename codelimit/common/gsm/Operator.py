from abc import ABC, abstractmethod

from codelimit.common.gsm.Automata import Automata


class Operator(ABC):
    @abstractmethod
    def apply(self, stack: list[Automata]):
        pass
