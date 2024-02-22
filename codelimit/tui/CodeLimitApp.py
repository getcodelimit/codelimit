from textual.app import App, ComposeResult
from textual.widgets import Footer

from codelimit.common.report.Report import Report
from codelimit.tui.CodebaseBrowserListView import CodebaseBrowserListView
from codelimit.tui.CodeLimitAppHeader import CodeLimitAppHeader
from codelimit.tui.CodeScreen import CodeScreen


class CodeLimitApp(App):
    BINDINGS = [("q", "quit", "Quit")]
    CSS = """
    ListItem {
        background: #020409;
    }
    ListView:focus > ListItem.--highlight {
        background: $accent;
    }
    """

    def __init__(self, report: Report):
        super().__init__()
        self.report = report
        self.code_screen = CodeScreen()

    def compose(self) -> ComposeResult:
        yield CodeLimitAppHeader(self.report)
        codebase_browser_list_view = CodebaseBrowserListView(self.report)
        yield codebase_browser_list_view
        self.set_focus(codebase_browser_list_view)
        # top_list_view = TopListView(self.report)
        # yield top_list_view
        # self.set_focus(top_list_view)
        yield Footer()
        self.install_screen(self.code_screen, "code_screen")

    async def on_unit_changed(self, message):
        await self.push_screen("code_screen")
        self.code_screen.set_code_snippet(message.file, message.snippet)

    def action_quit(self) -> None:
        self.exit()
