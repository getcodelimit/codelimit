class Location:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __str__(self):
        return f'{{line: {self.line}, column: {self.column}}}'
