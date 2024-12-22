from rich import box
from rich.table import Table
from rich.text import Text

from codelimit.common.report.Report import Report


class SummaryTable(Table):
    def __init__(self, report: Report):
        easy, verbose, hard_to_maintain, unmaintainable = report.quality_profile_percentage()
        super().__init__(expand=True, box=box.SIMPLE)
        self.add_column("Easy / Verbose", justify="right")
        self.add_column("Hard-to-maintain \u26A0", justify="right")
        self.add_column("Unmaintainable \u2716", justify="right")
        easy_verbose_text = Text(f"{easy + verbose:n}%")
        hard_to_maintain_text = Text(f"{hard_to_maintain:n}%")
        unmaintainable_text = Text(f"{unmaintainable:n}%")
        if unmaintainable > 0:
            unmaintainable_text.style = "red"
        if hard_to_maintain > 20:
            hard_to_maintain_text.style = "dark_orange"
        if unmaintainable == 0 and hard_to_maintain < 20:
            easy_verbose_text.style = "green"
        self.add_row(easy_verbose_text, hard_to_maintain_text, unmaintainable_text)
