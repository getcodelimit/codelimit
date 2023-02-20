from typing import Any

from textual.app import ComposeResult
from textual.binding import Binding
from textual.color import Color
from textual.containers import Content
from textual.screen import Screen
from textual.widgets import TextLog, Footer


class CodeScreen(Screen):
    BINDINGS = [('escape', 'close', 'Close'), Binding('left', 'close', 'Close', show=False)]

    def __init__(self):
        super().__init__()
        self.text_log = TextLog()
        self.text_log.styles.background = Color.parse('#272823')

    def compose(self) -> ComposeResult:
        yield Content(self.text_log)
        yield Footer()

    def set_code(self, code: Any):
        self.text_log.clear()
        self.text_log.write(code)
        self.text_log.scroll_home(animate=False)

    def action_close(self):
        self.app.pop_screen()
