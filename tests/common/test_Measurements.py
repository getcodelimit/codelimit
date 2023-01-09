from codelimit.common.Codebase import Codebase
from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportWriter import ReportWriter


def test_to_json():
    codebase = Codebase()
    codebase.add_file('foo.py', [SourceMeasurement('bar()', SourceLocation(10, 1), SourceLocation(20, 1), 10)])
    codebase.aggregate()
    report = Report(codebase)
    serializer = ReportWriter(report)

    expected = ''
    expected += '{\n'
    expected += '  "uuid": "' + report.uuid + '",\n'
    expected += '  "codebase": {\n'
    expected += '    "tree": {\n'
    expected += '      "./": {\n'
    expected += '        "entries": [\n'
    expected += '          {"name": "foo.py", "profile": [10, 0, 0, 0]}\n'
    expected += '        ],\n'
    expected += '        "profile": [10, 0, 0, 0]\n'
    expected += '      }\n'
    expected += '    },\n'
    expected += '    "measurements": {\n'
    expected += '      "foo.py": [\n'
    expected += '        {"unit_name": "bar()", "start": {"line": 10, "column": 1}, "end": {"line": 20, "column": 1}, "value": 10}\n'
    expected += '      ]\n'
    expected += '    }\n'
    expected += '  }\n'
    expected += '}\n'

    assert serializer.to_json() == expected


def test_to_json_multiple():
    codebase = Codebase()
    codebase.add_file('foo.py', [SourceMeasurement('bar()', SourceLocation(10, 1), SourceLocation(20, 1), 10)])
    codebase.add_file('bar.py', [SourceMeasurement('foo()', SourceLocation(20, 1), SourceLocation(30, 1), 10)])
    codebase.aggregate()
    report = Report(codebase)
    serializer = ReportWriter(report, False)

    expected = '{"uuid": "' + report.uuid + '", "codebase": {"tree": {"./": {"entries": [{"name": "foo.py", "profile": [10, 0, 0, 0]}, ' + \
               '{"name": "bar.py", "profile": [10, 0, 0, 0]}], "profile": [20, 0, 0, 0]}}, ' + \
               '"measurements": {"foo.py": [{"unit_name": "bar()", "start": {"line": 10, "column": 1}, ' + \
               '"end": {"line": 20, "column": 1}, "value": 10}], "bar.py": ' + \
               '[{"unit_name": "foo()", "start": {"line": 20, "column": 1}, ' + \
               '"end": {"line": 30, "column": 1}, "value": 10}]}}}'
    assert serializer.to_json() == expected


def test_all():
    measurements = Codebase()
    measurements.add_file('foo.py', [SourceMeasurement('bar()', SourceLocation(10, 1), SourceLocation(20, 1), 10)])
    measurements.add_file('bar.py', [SourceMeasurement('foo()', SourceLocation(20, 1), SourceLocation(30, 1), 10),
                                     SourceMeasurement('spam()', SourceLocation(30, 1), SourceLocation(40, 1), 10)])

    assert len(measurements.all_measurements()) == 3
