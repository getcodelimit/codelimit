from codelimit.common.gsm.State import State


class Pattern:
    def __init__(self, start: int, state: State):
        self.start = start
        self.state = state
        self.tokens: list = []
