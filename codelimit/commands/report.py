from pathlib import Path

import typer
from rich import print
from rich.console import Console

from codelimit.common.utils import format_measurement
from codelimit.utils import read_cached_report

REPORT_LENGTH = 10


def report_command(path: Path, full: bool):
    cwd = Path().resolve()
    if str(cwd) == str(path.absolute()):
        root = None
    elif path.absolute().is_relative_to(cwd):
        root = path
    else:
        root = path.absolute()
    report = read_cached_report(path)
    if not report:
        print("[red]No cached report found in current folder[/red]")
        raise typer.Exit(code=1)
    stdout = Console()
    units = report.all_report_units_sorted_by_length_asc(30)
    if len(units) == 0:
        print(
            "[bold]Refactoring not necessary, :sparkles: happy coding! :sparkles:[/bold]"
        )
        return
    if full:
        report_units = units
    else:
        report_units = units[0:REPORT_LENGTH]
    for unit in report_units:
        file_path = unit.file if root is None else root.joinpath(unit.file)
        stdout.print(
            format_measurement(str(file_path), unit.measurement), soft_wrap=True
        )
    if not full and len(units) > REPORT_LENGTH:
        print(
            f"[bold]{len(units) - REPORT_LENGTH} more rows, use --full option to get all rows[/bold]"
        )
