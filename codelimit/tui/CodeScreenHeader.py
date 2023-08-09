from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class CodeScreenHeader(Widget):
    def __init__(self):
        super().__init__()
        self.styles.dock = "top"
        self.styles.width = "100%"
        self.styles.height = 1

    def compose(self) -> ComposeResult:
        label = Label("-")
        label.styles.width = "100%"
        label.styles.content_align_horizontal = "center"
        yield label

    def set_title(self, title: str):
        self.query_one(Label).update(title)
