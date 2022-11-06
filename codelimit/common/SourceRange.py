from codelimit.common.Location import Location


class SourceRange:
    def __init__(self, start: Location, end: Location):
        self.start = start
        self.end = end

    def __str__(self):
        return f'[{self.start}, {self.end}]'

    def __repr__(self):
        return self.__str__()


class Header(SourceRange):
    pass


class Block(SourceRange):
    pass
