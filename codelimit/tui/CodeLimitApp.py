import os

from rich.syntax import Syntax
from textual.app import App, ComposeResult
from textual.widgets import Footer, ListView, ListItem, Label

from codelimit.common.report.Report import Report
from codelimit.common.source_utils import get_location_range
from codelimit.common.utils import format_unit, get_basename
from codelimit.tui.CodeLimitAppHeader import CodeLimitAppHeader
from codelimit.tui.CodeScreen import CodeScreen


class CodeLimitApp(App):
    TITLE = "A Question App"
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
        yield Footer()
        list_view = ListView()
        for idx, unit in enumerate(
            self.report.all_report_units_sorted_by_length_asc()[:100]
        ):
            list_item = ListItem(
                Label(
                    format_unit(
                        f"{get_basename(unit.file)}:{unit.measurement.unit_name}",
                        unit.measurement.value,
                    )
                ),
                name=f"{idx}",
            )
            list_view.append(list_item)
        yield list_view
        self.set_focus(list_view)
        self.install_screen(self.code_screen, "code_screen")

    def on_list_view_hightlighted(self, event: ListView.Highlighted):
        event.item.styles.background = "red"

    async def on_list_view_selected(self, event: ListView.Selected):
        idx = int(event.item.name)
        unit = self.report.all_report_units_sorted_by_length_asc()[idx]
        file_path = os.path.join(self.report.codebase.root, unit.file)
        with open(file_path) as file:
            code = file.read()
        snippet = get_location_range(code, unit.measurement.start, unit.measurement.end)
        rich_snippet = Syntax(snippet, "python", line_numbers=True)
        await self.push_screen("code_screen")
        self.code_screen.set_code_snippet(unit.file, rich_snippet)

    def action_quit(self) -> None:
        self.exit()
