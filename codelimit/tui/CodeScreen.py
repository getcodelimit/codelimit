from typing import Any

from textual.app import ComposeResult
from textual.binding import Binding
from textual.color import Color
from textual.containers import Content
from textual.screen import Screen
from textual.widgets import TextLog, Footer

from codelimit.tui.CodeScreenHeader import CodeScreenHeader


class CodeScreen(Screen):
    BINDINGS = [
        Binding("escape", "close", "Close", show=False),
        Binding("left", "close", "Close"),
    ]

    def __init__(self):
        super().__init__()
        self.text_log = TextLog()
        self.text_log.styles.background = Color.parse("#272823")
        self.header = CodeScreenHeader()

    def compose(self) -> ComposeResult:
        yield self.header
        yield Content(self.text_log)
        yield Footer()

    def set_code_snippet(self, title: str, code: Any):
        self.text_log.clear()
        self.text_log.write(code)
        self.text_log.scroll_home(animate=False)
        self.header.set_title(title)

    def action_close(self):
        self.app.pop_screen()
