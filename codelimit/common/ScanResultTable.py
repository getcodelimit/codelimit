from rich import box
from rich.table import Table
from rich.text import Text


class ScanResultTable(Table):
    def __init__(self, languages: dict):
        super().__init__(
            expand=True,
            box=box.SIMPLE,
        )
        self.languages = languages
        self.add_column("Language")
        self.add_column("Files", justify="right")
        self.add_column("Lines of Code", justify="right")
        self.add_column("Functions", justify="right")
        self.add_column("\u26A0", justify="right")
        self.add_column("\u2716", justify="right")
        self._populate()

    def _populate(self):
        for language, counts in self.languages.items():
            files = counts["files"]
            loc = counts["loc"]
            functions = counts["functions"]
            hard_to_maintain = counts["hard-to-maintain"]
            if hard_to_maintain > 0:
                hard_to_maintain_text = Text(
                    f"{hard_to_maintain:n}", style="dark_orange"
                )
            else:
                hard_to_maintain_text = "0"
            unmaintainable = counts["unmaintainable"]
            if unmaintainable > 0:
                unmaintainable_text = Text(f"{unmaintainable:n}", style="red")
            else:
                unmaintainable_text = "0"
            self.add_row(
                language,
                f"{files:n}",
                f"{loc:n}",
                f"{functions:n}",
                hard_to_maintain_text,
                unmaintainable_text,
            )
