from rich import box
from rich.table import Table
from rich.text import Text

from codelimit.common.ScanTotals import ScanTotals


class ScanResultTable(Table):
    def __init__(self, scan_totals: ScanTotals):
        super().__init__(
            expand=True, box=box.SIMPLE, show_footer=len(scan_totals.languages()) > 1
        )
        self.scan_totals = scan_totals
        self.add_column("Language")
        self.add_column("Files", f"{scan_totals.total_files():n}", justify="right")
        self.add_column(
            "Lines of Code", f"{scan_totals.total_loc():n}", justify="right"
        )
        self.add_column(
            "Functions", f"{scan_totals.total_functions():n}", justify="right"
        )
        self.add_column(
            "\u26A0", f"{scan_totals.total_hard_to_maintain():n}", justify="right"
        )
        self.add_column(
            "\u2716", f"{scan_totals.total_unmaintainable():n}", justify="right"
        )
        self._populate()

    def _populate(self):
        for language_totals in self.scan_totals.languages_totals():
            hard_to_maintain = language_totals.hard_to_maintain
            if hard_to_maintain > 0:
                hard_to_maintain_text = Text(
                    f"{hard_to_maintain:n}", style="dark_orange"
                )
            else:
                hard_to_maintain_text = "0"
            unmaintainable = language_totals.unmaintainable
            if unmaintainable > 0:
                unmaintainable_text = Text(f"{unmaintainable:n}", style="red")
            else:
                unmaintainable_text = "0"
            self.add_row(
                language_totals.language,
                f"{language_totals.files:n}",
                f"{language_totals.loc:n}",
                f"{language_totals.functions:n}",
                hard_to_maintain_text,
                unmaintainable_text,
            )
