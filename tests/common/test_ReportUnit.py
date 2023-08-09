from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.report.ReportUnit import format_report_unit, ReportUnit


def test_format_report_unit():
    report_unit = ReportUnit(
        "foo.py", Measurement("bar()", Location(10, 1), Location(11, 1), 1)
    )

    assert format_report_unit(report_unit).markup == "[[green]  1[/green]] bar()"

    report_unit = ReportUnit(
        "foo.py", Measurement("bar()", Location(10, 1), Location(30, 1), 20)
    )

    assert format_report_unit(report_unit).markup == "[[yellow] 20[/yellow]] bar()"

    report_unit = ReportUnit(
        "foo.py", Measurement("bar()", Location(10, 1), Location(80, 1), 70)
    )

    assert format_report_unit(report_unit).markup == "[[red]60+[/red]] bar()"
