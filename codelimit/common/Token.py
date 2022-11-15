from pygments.token import Keyword


class Token:
    def __init__(self, index: int, type: any, value: str):
        self.index = index
        self.type = type
        self.value = value

    def is_keyword(self):
        return self.type == Keyword
