from pathlib import Path

import typer
from rich.console import Console

from codelimit.common.utils import format_measurement
from codelimit.utils import read_cached_report


def report_command():
    report = read_cached_report(Path("."))
    if not report:
        print("[red]No cached report found in current folder[/red]")
        raise typer.Exit(code=1)
    stdout = Console()
    units = report.all_report_units_sorted_by_length_asc(30)
    for unit in units:
        stdout.print(format_measurement(unit.file, unit.measurement), soft_wrap=True)
