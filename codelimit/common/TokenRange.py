from codelimit.common.Token import Token


class TokenRange:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

    def __str__(self):
        return f'[{self.tokens[0].location}, {self.tokens[-1].location}]'

    def __repr__(self):
        return self.__str__()
