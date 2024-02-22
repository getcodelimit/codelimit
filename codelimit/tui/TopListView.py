import os

from rich.syntax import Syntax
from textual.widgets import ListItem, Label, ListView

from codelimit.common.report.Report import Report
from codelimit.common.source_utils import get_location_range
from codelimit.common.utils import format_unit, get_basename
from codelimit.tui.UnitChanged import UnitChanged


class TopListView(ListView):
    def __init__(self, report: Report):
        super().__init__()
        self.report = report
        self.load_report()

    def load_report(self):
        for idx, unit in enumerate(
            self.report.all_report_units_sorted_by_length_asc()[:100]
        ):
            list_item = ListItem(
                Label(
                    format_unit(
                        unit.measurement.unit_name,
                        unit.measurement.value,
                        get_basename(unit.file),
                    )
                ),
                name=f"{idx}",
            )
            self.append(list_item)

    async def on_list_view_selected(self, event: ListView.Selected):
        idx = int(event.item.name)
        unit = self.report.all_report_units_sorted_by_length_asc()[idx]
        file_path = os.path.join(self.report.codebase.root, unit.file)
        with open(file_path) as file:
            code = file.read()
        snippet = get_location_range(code, unit.measurement.start, unit.measurement.end)
        snippet_with_syntax_highlighting = Syntax(snippet, "python", line_numbers=True)
        self.post_message(UnitChanged(unit.file, snippet_with_syntax_highlighting))
