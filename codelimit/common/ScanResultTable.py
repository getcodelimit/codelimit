from rich import box
from rich.table import Table

from codelimit.common.LanguageTotalsDelta import LanguageTotalsDelta
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.ScanTotalsDelta import ScanTotalsDelta


class ScanResultTable(Table):
    def __init__(self, scan_totals_current: ScanTotals, scan_totals_previous: ScanTotals | None = None):
        super().__init__(
            expand=True, box=box.SIMPLE, show_footer=len(scan_totals_current.languages()) > 1
        )
        self._stc = scan_totals_current
        self._stp = scan_totals_previous
        self.add_column("Language")
        if self._stp:
            std = ScanTotalsDelta(self._stc, self._stp)
            self.add_column("Files", f"{std.total_files()}", justify="right")
            self.add_column("Functions", f"{std.total_functions()}", justify="right")
            self.add_column("Lines of Code", f"{std.total_loc()}", justify="right")
            self.add_column("\u26A0", f"{std.total_hard_to_maintain()}", justify="right")
            self.add_column("\u2716", f"{std.total_unmaintainable()}", justify="right")
        else:
            self.add_column("Files", f"{self._stc.total_files():n}", justify="right")
            self.add_column("Functions", f"{self._stc.total_functions():n}", justify="right")
            self.add_column("Lines of Code", f"{self._stc.total_loc():n}", justify="right")
            self.add_column("\u26A0", f"{self._stc.total_hard_to_maintain():n}", justify="right")
            self.add_column("\u2716", f"{self._stc.total_unmaintainable():n}", justify="right")
        self._populate()

    def _populate(self):
        for language_totals in self._stc.languages_totals():
            if self._stp:
                language_totals_previous = self._stc.language_total(language_totals.language)
                ltd = LanguageTotalsDelta(language_totals, language_totals_previous)
                self.add_row(
                    language_totals.language,
                    f"{ltd.files()}",
                    f"{ltd.functions()}",
                    f"{ltd.loc()}",
                    f"{ltd.hard_to_maintain()}",
                    f"{ltd.unmaintainable()}"
                )
            else:
                self.add_row(
                    language_totals.language,
                    f"{language_totals.files:n}",
                    f"{language_totals.functions:n}",
                    f"{language_totals.loc:n}",
                    f"{language_totals.hard_to_maintain:n}",
                    f"{language_totals.unmaintainable:n}"
                )
