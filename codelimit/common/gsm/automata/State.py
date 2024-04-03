from __future__ import annotations

from codelimit.common.gsm.predicate.Predicate import Predicate


class State:
    _id = 1

    def __init__(self) -> None:
        self.id = State._id
        State._id += 1
        self.transition: list[tuple[Predicate, State]] = []
        self.epsilon_transitions: list[State] = []

    def assign(self, state: State):
        self.id = state.id
        self.transition = state.transition
        self.epsilon_transitions = state.epsilon_transitions

    def __str__(self):
        return f"State({self.id})"

    def __repr__(self):
        result = "State("
        parts = [f"{self.id}"]
        for t in self.transition:
            parts.append(f"{t[0]} -> {t[1]}")
        for e in self.epsilon_transitions:
            parts.append(f"epsilon -> {e}")
        result += ", ".join(parts)
        result += ")"
        return result
