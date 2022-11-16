from codelimit.common.SourceRange import SourceRange


class Scope:
    def __init__(self, header: SourceRange, block: SourceRange):
        self.header = header
        self.block = block

    def __str__(self):
        return f'[{self.header.start}, {self.block.end}]'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.block.end.line - self.header.start.line + 1
