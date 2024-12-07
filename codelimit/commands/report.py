from enum import Enum
from pathlib import Path

import typer
from rich import print
from rich.console import Console
from rich.text import Text

from codelimit.common.ScanResultTable import ScanResultTable
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportUnit import ReportUnit
from codelimit.common.utils import format_measurement
from codelimit.utils import make_report_path

REPORT_LENGTH = 10


class ReportFormat(str, Enum):
    text = "text"
    markdown = "markdown"


def report_command(path: Path, full: bool, totals: bool, fmt: ReportFormat):
    stdout = Console()
    report = read_report(path)
    if totals:
        scan_totals = ScanTotals(report.codebase.totals)
        if fmt == ReportFormat.markdown:
            stdout.print(_report_totals_markdown(scan_totals), soft_wrap=True)
        else:
            stdout.print(ScanResultTable(scan_totals), soft_wrap=True)
    else:
        _report_functions(report, path, full, fmt, stdout)


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
    if len(st.languages_totals()) > 1:
        result += (
            f"| **Totals** | "
            f"**{st.total_files()}** | "
            f"**{st.total_loc()}** | "
            f"**{st.total_functions()}** | "
            f"**{st.total_hard_to_maintain()}** | "
            f"**{st.total_unmaintainable()}** |"
        )
    return result


def _report_functions(report: Report, path: Path, full: bool, fmt, console: Console):
    units = report.all_report_units_sorted_by_length_asc(30)
    if len(units) == 0:
        console.print(
            "[bold]Refactoring not necessary, :sparkles: happy coding! :sparkles:[/bold]"
        )
        return
    if full:
        report_units = units
    else:
        report_units = units[0:REPORT_LENGTH]
    root = get_root(path)
    if fmt == ReportFormat.markdown:
        console.print(_report_functions_markdown(root, report_units), soft_wrap=True)
    else:
        console.print(
            _report_functions_text(root, units, report_units, full), soft_wrap=True
        )


def get_root(path: Path) -> Path | None:
    cwd = Path().resolve()
    if str(cwd) == str(path.absolute()):
        return None
    elif path.absolute().is_relative_to(cwd):
        return path
    else:
        return path.absolute()


def read_report(path: Path) -> Report:
    report_path = make_report_path(path)
    if not report_path.exists():
        print("[red]No cached report found, run scan first[/red]")
        raise typer.Exit(code=1)
    report_data = report_path.read_text()
    report_version = ReportReader.get_report_version(report_data)
    if report_version != Report.VERSION:
        print("[red]Report version mismatch, run scan first[/red]")
        raise typer.Exit(code=1)
    return ReportReader.from_json(report_data)


def _report_functions_text(root, units, report_units, full) -> Text:
    result = Text()
    for unit in report_units:
        file_path = unit.file if root is None else root.joinpath(unit.file)
        result.append(format_measurement(str(file_path), unit.measurement).append("\n"))
    if not full and len(units) > REPORT_LENGTH:
        result.append(
            f"[bold]{len(units) - REPORT_LENGTH} more rows, use --full option to get all rows[/bold]\n"
        )
    return result


def _report_functions_markdown(
    root: Path | None, report_units: list[ReportUnit]
) -> str:
    result = ""
    result += "| **File** | **Line** | **Column** | **Length** | **Function** |\n"
    result += "| --- | ---: | ---: | ---: | --- |\n"
    for unit in report_units:
        file_path = unit.file if root is None else root.joinpath(unit.file)
        type = "✖" if unit.measurement.value > 60 else "⚠"
        result += (
            f"| {str(file_path)} | {unit.measurement.start.line} | {unit.measurement.start.column} | "
            f"{unit.measurement.value} | {type} {unit.measurement.unit_name} |\n"
        )
    return result
