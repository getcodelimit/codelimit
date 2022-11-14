from codelimit.common.SourceLocation import SourceLocation


class SourceRange:
    def __init__(self, start: SourceLocation, end: SourceLocation):
        self.start = start
        self.end = end

    def __str__(self):
        return f'[{self.start}, {self.end}]'

    def __repr__(self):
        return self.__str__()
