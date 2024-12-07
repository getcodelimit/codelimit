from codelimit.commands.report import (
    _report_totals_markdown,
    _report_functions_markdown,
)
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
    result = _report_totals_markdown(st)

    assert result == (
        "| **Language** | **Files** | **Lines of Code** | **Functions** | ⚠ | ✖ |\n"
        "| --- | ---: | ---: | ---: | ---: | ---: |\n"
        "| Python | 1 | 2 | 3 | 4 | 5 |\n"
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
    result = _report_totals_markdown(st)

    assert result == (
        "| **Language** | **Files** | **Lines of Code** | **Functions** | ⚠ | ✖ |\n"
        "| --- | ---: | ---: | ---: | ---: | ---: |\n"
        "| Python | 1 | 2 | 3 | 4 | 5 |\n"
        "| TypeScript | 1 | 2 | 3 | 4 | 5 |\n"
        "| **Totals** | **2** | **4** | **6** | **8** | **10** |"
    )


def test_print_functions_markdown():
    result = _report_functions_markdown(
        None,
        [
            ReportUnit(
                "foo.py", Measurement("bar()", Location(1, 1), Location(30, 1), 31)
            )
        ],
    )

    assert result == (
        "| **File** | **Line** | **Column** | **Length** | **Function** |\n"
        "| --- | ---: | ---: | ---: | --- |\n"
        "| foo.py | 1 | 1 | 31 | ⚠ bar() |\n"
    )
