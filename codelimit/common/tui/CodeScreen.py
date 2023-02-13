from typing import Any

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import TextLog, Footer


class CodeScreen(Screen):
    BINDINGS = [('escape', 'close', 'Close')]

    def __init__(self):
        super().__init__()
        self.text_log = TextLog()

    def compose(self) -> ComposeResult:
        yield Container(self.text_log)
        yield Footer()

    def set_code(self, code: Any):
        self.text_log.clear()
        self.text_log.write(code)

    def action_close(self):
        self.app.pop_screen()
