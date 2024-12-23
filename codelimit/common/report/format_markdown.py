from rich.console import Console

from codelimit.common.GithubRepository import GithubRepository
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportUnit import ReportUnit


def print_report(report: Report, console: Console):
    print_totals(report, console)
    print_summary(report, console)


def print_totals(report, console):
    console.print("### Overview")
    _print_totals(ScanTotals(report.codebase.totals), console)
    console.print("")


def print_summary(report: Report, console: Console):
    console.print("### Summary")
    easy, verbose, hard_to_maintain, unmaintainable = report.quality_profile_percentage()
    console.print("| **Easy / Verbose** | **Hard-to-maintain \u26A0** | **Unmaintainable \u274C** |")
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


def _print_totals(st: ScanTotals, console: Console):
    console.print(
        "| **Language** | **Files** | **Lines of Code** | **Functions** | **\u26A0** | **\u274C** |"
    )
    console.print("| --- | ---: | ---: | ---: | ---: | ---: |")
    for lt in st.languages_totals():
        console.print(
            f"| {lt.language} | "
            f"{lt.files} | "
            f"{lt.loc} | "
            f"{lt.functions} | "
            f"{lt.hard_to_maintain} | "
            f"{lt.unmaintainable} |"
        )
    if len(st.languages_totals()) > 1:
        console.print(
            f"| **Totals** | "
            f"**{st.total_files()}** | "
            f"**{st.total_loc()}** | "
            f"**{st.total_functions()}** | "
            f"**{st.total_hard_to_maintain()}** | "
            f"**{st.total_unmaintainable()}** |"
        )


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
            f"| {violation_type} \[{unit.measurement.unit_name}]({link}) | {unit.measurement.value} | {unit.file} |"
        )
