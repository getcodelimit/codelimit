from rich.syntax import Syntax
from textual.message import Message


class UnitChanged(Message):
    def __init__(self, file: str, snippet: Syntax):
        super().__init__()
        self.file = file
        self.snippet = snippet
