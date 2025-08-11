import os
from os.path import relpath
from pathlib import Path

import rich
from rich.console import Console

from codelimit.common.Measurement import Measurement
from codelimit.common.utils import format_measurement


class CheckResult:
    def __init__(self) -> None:
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
                if cwd_path in file.parents:
                    file_path = str(relpath(file, cwd_path))
                else:
                    file_path = str(file)
                stdout.print(format_measurement(file_path, m), soft_wrap=True)
        if self.hard_to_maintain > 0 or self.unmaintainable > 0:
            file_list_len = len(self.file_list)
            need_refactoring = self.hard_to_maintain + self.unmaintainable
            rich.print(
                f"{len(self.file_list)} {'file' if file_list_len == 1 else 'files'} checked, "
                f"{need_refactoring} {'function needs' if need_refactoring == 1 else 'functions need'} "
                f"refactoring."
            )
        else:
            rich.print(
                f"{len(self.file_list)} files checked, :sparkles: Refactoring not "
                f"necessary :sparkles:, happy coding!"
            )
