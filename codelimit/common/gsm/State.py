from __future__ import annotations


class State:
    _id = 1

    def __init__(self):
        self.id = State._id
        State._id += 1
        self.transition: tuple[str, State] | None = None
        self.epsilon_transitions: list[State] | None = None

    def assign(self, state: State):
        self.id = state.id
        self.transition = state.transition
        self.epsilon_transitions = state.epsilon_transitions

    def is_accepting(self):
        return self.transition is None and self.epsilon_transitions is None

    def __repr__(self):
        result = f'State({self.id}, '
        if self.is_accepting():
            result += 'F'
        else:
            parts = []
            if self.transition:
                parts.append(f'{self.transition[0]} -> {self.transition[1]}')
            if self.epsilon_transitions:
                for t in self.epsilon_transitions:
                    parts.append(f'epsilon -> {t}')
            result += ', '.join(parts)
        result += ')'
        return result
