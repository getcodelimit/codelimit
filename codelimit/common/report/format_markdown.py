from rich.console import Console

from codelimit.common.GithubRepository import GithubRepository
from codelimit.common.LanguageTotalsDelta import LanguageTotalsDelta
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.ScanTotalsDelta import ScanTotalsDelta
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportUnit import ReportUnit


def print_report(console: Console, report: Report, diff_report: Report | None = None):
    print_totals(console, report, diff_report)
    print_summary(console, report)


def print_totals(console: Console, report: Report, diff_report: Report | None = None):
    console.print("### Overview")
    scan_totals = ScanTotals(report.codebase.totals)
    if diff_report:
        _print_totals(console, scan_totals, ScanTotals(diff_report.codebase.totals))
    else:
        _print_totals(console, scan_totals)
    console.print("")


def _print_totals(console: Console, scan_totals_current: ScanTotals, scan_totals_previous: ScanTotals | None = None):
    console.print(
        "| **Language** | **Files** | **Functions** | **Lines of Code** | **\u26A0** | **\u26CC** |"
    )
    console.print("| --- | ---: | ---: | ---: | ---: | ---: |")
    for language_totals in scan_totals_current.languages_totals():
        if scan_totals_previous:
            language_totals_previous = scan_totals_previous.language_total(language_totals.language)
            ltd = LanguageTotalsDelta(language_totals, language_totals_previous)
            console.print(
                language_totals.language,
                f"| {ltd.files()} | ",
                f"{ltd.functions()} | ",
                f"{ltd.loc()} | ",
                f"{ltd.hard_to_maintain()} | ",
                f"{ltd.unmaintainable()} |"
            )
        else:
            console.print(
                f"| {language_totals.language} | "
                f"{language_totals.files} | "
                f"{language_totals.functions} | "
                f"{language_totals.loc} | "
                f"{language_totals.hard_to_maintain} | "
                f"{language_totals.unmaintainable} |"
            )
    if len(scan_totals_current.languages_totals()) > 1:
        if scan_totals_previous:
            std = ScanTotalsDelta(scan_totals_current, scan_totals_previous)
            console.print(
                f"| **Totals** | "
                f"**{std.total_files()}** | "
                f"**{std.total_functions()}** | "
                f"**{std.total_loc()}** | "
                f"**{std.total_hard_to_maintain()}** | "
                f"**{std.total_unmaintainable()}** |"
            )
        else:
            console.print(
                f"| **Totals** | "
                f"**{scan_totals_current.total_files()}** | "
                f"**{scan_totals_current.total_functions()}** | "
                f"**{scan_totals_current.total_loc()}** | "
                f"**{scan_totals_current.total_hard_to_maintain()}** | "
                f"**{scan_totals_current.total_unmaintainable()}** |"
            )


def print_summary(console: Console, report: Report):
    console.print("### Summary")
    easy, verbose, hard_to_maintain, unmaintainable = report.quality_profile_percentage()
    console.print("| **Easy / Verbose** | **Hard-to-maintain \u26A0** | **Unmaintainable \u26CC** |")
    console.print("| ---: | ---: | ---: |")
    console.print(f"| {easy + verbose}% | {hard_to_maintain}% | {unmaintainable}% |")
    console.print("")
    if unmaintainable > 0:
        console.print(f":stop_sign: {unmaintainable}% of the functions are unmaintainable, refactoring necessary.")
    elif hard_to_maintain > 20:
        console.print(f":warning: {hard_to_maintain}% of the functions are hard to maintain, refactoring necessary.")
    else:
        console.print(
            f":white_check_mark: {easy + verbose}% of the functions are maintainable, no refactoring necessary.")
    console.print("")


def print_findings(report: Report, console: Console, full: bool = False):
    functions = report.all_report_units_sorted_by_length_asc(30)
    total_findings = len(functions)
    if not full and total_findings > 10:
        functions = functions[:10]
    if report.repository:
        _print_findings_with_repository(functions, report.repository, console)
    else:
        _print_findings_without_repository(functions, console)
    if not full and total_findings > 10:
        console.print()
        console.print(f"{total_findings - 10} more rows", style="bold")


def _print_findings_without_repository(report_units: list[ReportUnit], console: Console):
    console.print("| **File** | **Line** | **Column** | **Length** | **Function** |")
    console.print("| --- | ---: | ---: | ---: | --- |")
    for unit in report_units:
        file_path = unit.file
        type = "\u274C" if unit.measurement.value > 60 else "\u26A0"
        console.print(
            f"| {str(file_path)} | {unit.measurement.start.line} | {unit.measurement.start.column} | "
            f"{unit.measurement.value} | {type} {unit.measurement.unit_name} |"
        )


def _print_findings_with_repository(report_units: list[ReportUnit],
                                    repository: GithubRepository, console: Console):
    console.print("| **Function** | **Length** | **File** |")
    console.print("| --- | ---: | --- |")
    for unit in report_units:
        violation_type = "\u274C" if unit.measurement.value > 60 else "\u26A0"
        owner = repository.owner
        name = repository.name
        branch = repository.branch
        link = (f'https://github.com/{owner}/{name}/blob/{branch}/{unit.file}#L{unit.measurement.start.line}-L'
                f'{unit.measurement.end.line}')
        console.print(
            f"| {violation_type} " + '\[' + unit.measurement.unit_name + ']' + f"({link}) | {unit.measurement.value} "
                                                                               f"| {unit.file} |"
        )
