from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.report.ReportUnit import format_report_unit, ReportUnit


def test_format_report_unit():
    report_unit = ReportUnit('foo.py', SourceMeasurement('bar()', SourceLocation(10, 1), SourceLocation(11, 1), 1))

    assert format_report_unit(report_unit) == '🟢 [  1] bar()'

    report_unit = ReportUnit('foo.py', SourceMeasurement('bar()', SourceLocation(10, 1), SourceLocation(30, 1), 20))

    assert format_report_unit(report_unit) == '🟡 [ 20] bar()'

    report_unit = ReportUnit('foo.py', SourceMeasurement('bar()', SourceLocation(10, 1), SourceLocation(80, 1), 70))

    assert format_report_unit(report_unit) == '🔴 [60+] bar()'
