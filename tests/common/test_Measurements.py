from codelimit.common.Codebase import Codebase
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportWriter import ReportWriter


def test_to_json():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("bar()", Location(10, 1), Location(20, 1), 10)],
        )
    )
    codebase.aggregate()
    report = Report(codebase)
    serializer = ReportWriter(report)

    expected = ""
    expected += "{\n"
    expected += '  "version": "' + report.version + '",\n'
    expected += '  "uuid": "' + report.uuid + '",\n'
    expected += '  "timestamp": "' + report.timestamp + '",\n'
    expected += '  "root": "/",\n'
    expected += '  "codebase": {\n'
    expected += '    "totals": {\n'
    expected += '      "Python": {\n'
    expected += '        "files": 1,\n'
    expected += '        "lines_of_code": 20,\n'
    expected += '        "functions": 1,\n'
    expected += '        "hard_to_maintain": 0,\n'
    expected += '        "unmaintainable": 0\n'
    expected += "      }\n"
    expected += "    },\n"
    expected += '    "tree": {\n'
    expected += '      "./": {\n'
    expected += '        "entries": [\n'
    expected += '          "foo.py"\n'
    expected += "        ],\n"
    expected += '        "profile": [10, 0, 0, 0]\n'
    expected += "      }\n"
    expected += "    },\n"
    expected += '    "files": {\n'
    expected += '      "foo.py": {\n'
    expected += '        "checksum": "abcd1234",\n'
    expected += '        "language": "Python",\n'
    expected += '        "loc": 20,\n'
    expected += '        "profile": [10, 0, 0, 0],\n'
    expected += '        "measurements": [\n'
    expected += (
        '          {"unit_name": "bar()", "start": {"line": 10, "column": 1}, '
        '"end": {"line": 20, "column": 1}, "value": 10}\n'
    )
    expected += "        ]\n"
    expected += "      }\n"
    expected += "    }\n"
    expected += "  }\n"
    expected += "}\n"

    assert serializer.to_json() == expected


def test_to_json_multiple():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("bar()", Location(10, 1), Location(20, 1), 10)],
        )
    )
    codebase.add_file(
        SourceFileEntry(
            "bar.py",
            "efgh5678",
            "Python",
            20,
            [Measurement("foo()", Location(20, 1), Location(30, 1), 10)],
        )
    )
    codebase.aggregate()
    report = Report(codebase)
    serializer = ReportWriter(report, False)

    expected = (
        f'{{"version": "{report.version}", "uuid": "{report.uuid}", '
        f'"timestamp": "{report.timestamp}", '
        '"root": "/", "codebase": {"totals": {"Python": {"files": 2, "lines_of_code": '
        '40, "functions": 2, "hard_to_maintain": 0, "unmaintainable": 0}}, "tree": '
        '{"./": {"entries": ["foo.py", "bar.py"], "profile": [20, 0, 0, 0]}}, '
        '"files": {"foo.py": {"checksum": "abcd1234", "language": "Python", "loc": '
        '20, "profile": [10, 0, 0, 0], "measurements": [{"unit_name": "bar()", '
        '"start": {"line": 10, "column": 1}, "end": {"line": 20, "column": 1}, '
        '"value": 10}]}, "bar.py": {"checksum": "efgh5678", "language": "Python", '
        '"loc": 20, "profile": [10, 0, 0, 0], "measurements": [{"unit_name": "foo()", '
        '"start": {"line": 20, "column": 1}, "end": {"line": 30, "column": 1}, '
        '"value": 10}]}}}}'
    )
    assert serializer.to_json() == expected


def test_all():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("bar()", Location(10, 1), Location(20, 1), 10)],
        )
    )
    codebase.add_file(
        SourceFileEntry(
            "bar.py",
            "efgh5678",
            "Python",
            20,
            [
                Measurement("foo()", Location(20, 1), Location(30, 1), 10),
                Measurement("spam()", Location(30, 1), Location(40, 1), 10),
            ],
        )
    )

    assert len(codebase.all_measurements()) == 3
