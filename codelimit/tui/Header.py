import webbrowser

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static

from codelimit.version import version


class Header(Widget):
    def __init__(self, *children: Widget):
        super().__init__(*children)
        self.styles.dock = 'top'
        self.styles.width = '100%'
        self.styles.height = 1

    def compose(self) -> ComposeResult:
        yield HeaderLeft()


class HeaderLeft(Static):
    def __init__(self, *children: Widget):
        super().__init__(*children)
        self.styles.dock = 'left'

    def render(self) -> str:
        return f'CodeLimit v.{version}'

    def on_click(self) -> None:
        webbrowser.open('https://github.com/getcodelimit/codelimit')
