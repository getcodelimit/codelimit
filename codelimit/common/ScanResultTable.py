from rich import box
from rich.table import Table

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
            self.add_row(
                language_totals.language,
                f"{language_totals.files:n}",
                f"{language_totals.loc:n}",
                f"{language_totals.functions:n}",
                f"{language_totals.hard_to_maintain:n}",
                f"{language_totals.unmaintainable:n}"
            )
