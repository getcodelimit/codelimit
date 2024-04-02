from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class Predicate(ABC, Generic[T]):

    @abstractmethod
    def accept(self, item: T) -> bool:
        pass
