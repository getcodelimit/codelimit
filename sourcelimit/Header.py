from sourcelimit.Position import Position


class Header:
    def __init__(self, start: Position, end: Position):
        self.start = start
        self.end = end

    def __str__(self):
        return f'[{self.start}, {self.end}]'

    def __repr__(self):
        return self.__str__()

