from __future__ import annotations


class State:
    _id = 1

    def __init__(self):
        self.id = State._id
        State._id += 1
        self.transition: tuple[str, State] | list[tuple[str, State]] | None = None
        self.epsilon_transitions: list[State] | None = None

    def assign(self, state: State):
        self.id = state.id
        self.transition = state.transition
        self.epsilon_transitions = state.epsilon_transitions

    def __str__(self):
        return f'State({self.id})'

    def __repr__(self):
        result = 'State('
        parts = [f'{self.id}']
        if self.transition:
            if isinstance(self.transition, list):
                for t in self.transition:
                    parts.append(f'{t[0]} -> {t[1]}')
            else:
                parts.append(f'{self.transition[0]} -> {self.transition[1]}')
        if self.epsilon_transitions:
            for t in self.epsilon_transitions:
                parts.append(f'epsilon -> {t}')
        result += ', '.join(parts)
        result += ')'
        return result
