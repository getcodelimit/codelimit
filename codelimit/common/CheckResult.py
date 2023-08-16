import os
from os.path import relpath
from pathlib import Path

import rich
from rich.console import Console
from rich.style import Style
from rich.text import Text

from codelimit.common.Measurement import Measurement
from codelimit.common.utils import format_unit


class CheckResult:
    def __init__(self):
        self.file_list: list[tuple[Path, list[Measurement]]] = []
        self.hard_to_maintain = 0
        self.unmaintainable = 0

    def add(self, file: Path, measurements: list[Measurement]):
        self.file_list.append((file, measurements))
        self.hard_to_maintain += len([m for m in measurements if 30 < m.value <= 60])
        self.unmaintainable += len([m for m in measurements if m.value > 60])

    def __len__(self):
        return len(self.file_list)

    def report(self):
        cwd_path = Path(os.getcwd())
        stdout = Console()
        for file, measurements in self.file_list:
            for m in measurements:
                text = Text()
                if cwd_path in file.parents:
                    text.append(relpath(file, cwd_path), style=Style(bold=True))
                else:
                    text.append(str(file), style="bold")
                text.append(":", style=Style(color="cyan"))
                text.append(str(m.start.line))
                text.append(":", style=Style(color="cyan"))
                text.append(str(m.start.column))
                text.append(":", style=Style(color="cyan"))
                text.append(" ")
                text.append(format_unit(m.unit_name, m.value))
                stdout.print(text, soft_wrap=True)
        if self.hard_to_maintain > 0 or self.unmaintainable > 0:
            rich.print(
                f"{len(self.file_list)} files checked, "
                f"{self.hard_to_maintain + self.unmaintainable} functions need "
                f"refactoring."
            )
        else:
            rich.print(
                f"{len(self.file_list)} files checked, :sparkles: Refactoring not "
                f"necessary :sparkles:, happy coding!"
            )
