from math import ceil

from rich.console import Console

from codelimit.common.ScanResultTable import ScanResultTable
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.SummaryTable import SummaryTable
from codelimit.common.report.Report import Report
from codelimit.common.utils import format_measurement


def print_report(report: Report, console: Console):
    print_totals(report, console)
    print_summary(report, console)


def print_totals(report: Report, console: Console):
    print_totals_header(console)
    console.print(ScanResultTable(ScanTotals(report.codebase.totals)))


def print_totals_header(console: Console):
    console.print('[u][b]Overview[/b][/u]', justify="center")


def make_profile(report: Report) -> str:
    result = ""
    easy, verbose, hard_to_maintain, unmaintainable = report.quality_profile_percentage()
    red_squares = ceil(unmaintainable / 10)
    orange_squares = ceil(hard_to_maintain / 10)
    green_squares = 10 - red_squares - orange_squares
    result += (f"{':green_square:' * green_squares}{':orange_square:' * orange_squares}"
               f"{':red_square:' * red_squares}\n")
    return result


def print_summary(report: Report, console: Console):
    console.print('[u][b]Summary[/b][/u]', justify="center")
    console.print(SummaryTable(report))
    easy, verbose, hard_to_maintain, unmaintainable = report.quality_profile_percentage()
    if unmaintainable > 0:
        console.print(f":stop_sign: {unmaintainable}% of lines of code are unmaintainable, refactoring necessary.",
                      highlight=False, justify="center")
    elif hard_to_maintain > 20:
        console.print(f":warning: {hard_to_maintain}% of the functions are hard to maintain, refactoring necessary.",
                      highlight=False, justify="center")
    else:
        console.print(
            f":white_check_mark: {easy + verbose}% of lines of code are maintainable, no refactoring necessary.",
            highlight=False, justify="center")


def print_findings(report: Report, console: Console, full: bool = False):
    functions = report.all_report_units_sorted_by_length_asc(30)
    total_findings = len(functions)
    if not full and total_findings > 10:
        functions = functions[:10]
    for function in functions:
        console.print(format_measurement(function.file, function.measurement))
    if not full and total_findings > 10:
        console.print(
            f"{total_findings - 10} more rows, use --full option to get all rows\n", style="bold"
        )
