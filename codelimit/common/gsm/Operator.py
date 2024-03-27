from abc import ABC, abstractmethod

from codelimit.common.gsm.NFA import NFA


class Operator(ABC):
    @abstractmethod
    def apply(self, stack: list[NFA]):
        pass
