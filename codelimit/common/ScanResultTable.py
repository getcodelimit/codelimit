from rich import box
from rich.table import Table
from rich.text import Text

from codelimit.common.ScanTotals import ScanTotals


class ScanResultTable(Table):
    def __init__(self, scan_totals: ScanTotals):
        super().__init__(
            expand=True,
            box=box.SIMPLE,
        )
        self.scan_totals = scan_totals
        self.add_column("Language")
        self.add_column("Files", justify="right")
        self.add_column("Lines of Code", justify="right")
        self.add_column("Functions", justify="right")
        self.add_column("\u26A0", justify="right")
        self.add_column("\u2716", justify="right")
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
