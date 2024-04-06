from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Predicate(ABC, Generic[T]):

    @abstractmethod
    def accept(self, item: T) -> bool:
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def __hash__(self):
        pass
