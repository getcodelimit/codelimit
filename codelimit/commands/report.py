from pathlib import Path

import typer
from rich.console import Console
from rich import print

from codelimit.common.utils import format_measurement
from codelimit.utils import read_cached_report


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
    if full:
        report_units = units
    else:
        report_units = units[0:100]
    for unit in report_units:
        file_path = unit.file if root is None else root.joinpath(unit.file)
        stdout.print(format_measurement(str(file_path), unit.measurement), soft_wrap=True)
    if not full and len(units) > 100:
        print(f"[bold]{len(units) - 100} more rows, use --full option to get all rows[/bold]")
