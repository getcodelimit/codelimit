from typing import Any

from codelimit.common.gsm.predicate.Predicate import Predicate


class Identity(Predicate[Any]):

    def __init__(self, item: Any):
        self.item = item

    def accept(self, item: Any) -> bool:
        return self.item == item

    def __str__(self):
        return f"{self.item}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Identity):
            return False
        return self.item == other.item

    def __hash__(self):
        return hash(self.item)
