from codelimit.common.SourceRange import SourceRange


class Scope:
    def __init__(self, header: SourceRange, block: SourceRange):
        self.header = header
        self.block = block

    def __str__(self):
        return f'{{header: {self.header}, block: {self.block}}}'

    def __repr__(self):
        return self.__str__()
