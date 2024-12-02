from enum import Enum
from pathlib import Path

import typer
from rich import print
from rich.console import Console

from codelimit.common.ScanResultTable import ScanResultTable
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportUnit import ReportUnit
from codelimit.common.utils import format_measurement
from codelimit.utils import read_cached_report

REPORT_LENGTH = 10


class ReportFormat(str, Enum):
    text = "text"
    markdown = "markdown"


def report_command(path: Path, full: bool, totals: bool, fmt: ReportFormat):
    report = read_report(path)
    if totals:
        scan_totals = ScanTotals(report.codebase.totals)
        if fmt == ReportFormat.markdown:
            print(_report_totals_markdown(scan_totals))
        else:
            _report_totals_text(scan_totals)
    else:
        _report_units(report, path, full, fmt)


def _report_totals_text(scan_totals: ScanTotals):
    table = ScanResultTable(scan_totals)
    print(table)


def _report_totals_markdown(st: ScanTotals) -> str:
    result = ""
    result += (
        "| **Language** | **Files** | **Lines of Code** | **Functions** | ⚠ | ✖ |\n"
    )
    result += "| --- | ---: | ---: | ---: | ---: | ---: |\n"
    for lt in st.languages_totals():
        result += (
            f"| {lt.language} | "
            f"{lt.files} | "
            f"{lt.loc} | "
            f"{lt.functions} | "
            f"{lt.hard_to_maintain} | "
            f"{lt.unmaintainable} |\n"
        )
    result += (
        f"| | "
        f"**{st.total_files()}** | "
        f"**{st.total_loc()}** | "
        f"**{st.total_functions()}** | "
        f"**{st.total_hard_to_maintain()}** | "
        f"**{st.total_unmaintainable()}** |"
    )
    return result


def _report_units(report: Report, path: Path, full: bool, fmt):
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
    root = get_root(path)
    if fmt == ReportFormat.markdown:
        _print_functions_markdown(root, report_units)
    else:
        _print_functions_text(root, units, report_units, full)


def get_root(path: Path) -> Path | None:
    cwd = Path().resolve()
    if str(cwd) == str(path.absolute()):
        return None
    elif path.absolute().is_relative_to(cwd):
        return path
    else:
        return path.absolute()


def read_report(path: Path) -> Report:
    report = read_cached_report(path)
    if not report:
        print("[red]No cached report found in current folder[/red]")
        raise typer.Exit(code=1)
    return report


def _print_functions_text(root, units, report_units, full):
    stdout = Console()
    for unit in report_units:
        file_path = unit.file if root is None else root.joinpath(unit.file)
        stdout.print(
            format_measurement(str(file_path), unit.measurement), soft_wrap=True
        )
    if not full and len(units) > REPORT_LENGTH:
        print(
            f"[bold]{len(units) - REPORT_LENGTH} more rows, use --full option to get all rows[/bold]"
        )


def _print_functions_markdown(root: Path | None, report_units: list[ReportUnit]) -> str:
    result = ""
    result += "| **File** | **Line** | **Column** | **Length** | **Function** |\n"
    result += "| --- | ---: | ---: | ---: | --- |\n"
    for unit in report_units:
        file_path = unit.file if root is None else root.joinpath(unit.file)
        result += (
            f"| {str(file_path)} | {unit.measurement.start.line} | {unit.measurement.start.column} | "
            f"{unit.measurement.value} | {unit.measurement.unit_name} |\n"
        )
    return result
