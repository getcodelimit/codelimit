from rich.console import Console

from codelimit.common.report import format_markdown
from codelimit.common.LanguageTotals import LanguageTotals
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.report.ReportUnit import ReportUnit


def test_report_totals_markdown_one_language():
    python_totals = LanguageTotals("Python")
    python_totals.files = 1
    python_totals.loc = 2
    python_totals.functions = 3
    python_totals.hard_to_maintain = 4
    python_totals.unmaintainable = 5
    st = ScanTotals({"Python": python_totals})
    console = Console(record=True, soft_wrap=True)
    format_markdown._print_totals(console, st)

    assert console.export_text() == (
        "| **Language** | **Files** | **Functions** | **Lines of Code** | **\u26A0** | **\u26CC** |\n"
        "| --- | ---: | ---: | ---: | ---: | ---: |\n"
        "| Python | 1 | 3 | 2 | 4 | 5 |\n"
    )


def test_report_totals_markdown_two_languages():
    python_totals = LanguageTotals("Python")
    python_totals.files = 1
    python_totals.loc = 2
    python_totals.functions = 3
    python_totals.hard_to_maintain = 4
    python_totals.unmaintainable = 5
    ts_totals = LanguageTotals("TypeScript")
    ts_totals.files = 1
    ts_totals.loc = 2
    ts_totals.functions = 3
    ts_totals.hard_to_maintain = 4
    ts_totals.unmaintainable = 5
    st = ScanTotals({"Python": python_totals, "TypeScript": ts_totals})
    console = Console(record=True, soft_wrap=True)
    format_markdown._print_totals(console, st)

    assert console.export_text() == (
        "| **Language** | **Files** | **Functions** | **Lines of Code** | **\u26A0** | **\u26CC** |\n"
        "| --- | ---: | ---: | ---: | ---: | ---: |\n"
        "| Python | 1 | 3 | 2 | 4 | 5 |\n"
        "| TypeScript | 1 | 3 | 2 | 4 | 5 |\n"
        "| **Totals** | **2** | **6** | **4** | **8** | **10** |\n"
    )


def test_print_functions_markdown():
    console = Console(record=True, soft_wrap=True)
    format_markdown._print_findings_without_repository(
        [
            ReportUnit(
                "foo.py", Measurement("bar()", Location(1, 1), Location(30, 1), 31)
            )
        ],
    console)

    assert console.export_text() == (
        "| **File** | **Line** | **Column** | **Length** | **Function** |\n"
        "| --- | ---: | ---: | ---: | --- |\n"
        "| foo.py | 1 | 1 | 31 | ⚠ bar() |\n"
    )
