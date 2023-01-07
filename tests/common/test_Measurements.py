from codelimit.common.Codebase import Codebase
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.common.SourceMeasurement import SourceMeasurement


def test_to_json():
    codebase = Codebase()
    codebase.add_file('foo.py', [SourceMeasurement(10, 10)])
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
    expected += '        {"start_line": 10, "value": 10}\n'
    expected += '      ]\n'
    expected += '    }\n'
    expected += '  }\n'
    expected += '}\n'

    assert serializer.to_json() == expected


def test_to_json_multiple():
    codebase = Codebase()
    codebase.add_file('foo.py', [SourceMeasurement(10, 10)])
    codebase.add_file('bar.py', [SourceMeasurement(20, 10)])
    codebase.aggregate()
    report = Report(codebase)
    serializer = ReportWriter(report, False)

    expected = '{"uuid": "' + report.uuid + '", "codebase": {"tree": {"./": {"entries": [{"name": "foo.py", "profile": [10, 0, 0, 0]}, ' + \
               '{"name": "bar.py", "profile": [10, 0, 0, 0]}], "profile": [20, 0, 0, 0]}}, ' + \
               '"measurements": {"foo.py": [{"start_line": 10, "value": 10}], "bar.py": ' + \
               '[{"start_line": 20, "value": 10}]}}}'
    assert serializer.to_json() == expected


def test_all():
    measurements = Codebase()
    measurements.add_file('foo.py', [SourceMeasurement(10, 10)])
    measurements.add_file('bar.py', [SourceMeasurement(20, 10), SourceMeasurement(30, 10)])

    assert len(measurements.all_measurements()) == 3
