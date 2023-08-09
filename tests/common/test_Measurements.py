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
            [Measurement("bar()", Location(10, 1), Location(20, 1), 10)],
        )
    )
    codebase.aggregate()
    report = Report(codebase)
    serializer = ReportWriter(report)

    expected = ""
    expected += "{\n"
    expected += '  "uuid": "' + report.uuid + '",\n'
    expected += '  "root": "/",\n'
    expected += '  "codebase": {\n'
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
            [Measurement("bar()", Location(10, 1), Location(20, 1), 10)],
        )
    )
    codebase.add_file(
        SourceFileEntry(
            "bar.py",
            "efgh5678",
            [Measurement("foo()", Location(20, 1), Location(30, 1), 10)],
        )
    )
    codebase.aggregate()
    report = Report(codebase)
    serializer = ReportWriter(report, False)

    expected = (
        '{"uuid": "'
        + report.uuid
        + '", "root": "/", "codebase": {"tree": {"./": {"entries": ["foo.py", '
        + '"bar.py"], "profile": [20, 0, 0, 0]}}, '
        + '"files": {"foo.py": {"checksum": "abcd1234", "profile": [10, 0, 0, 0], '
        '"measurements": '
        + '[{"unit_name": "bar()", "start": {"line": 10, "column": 1}, '
        + '"end": {"line": 20, "column": 1}, "value": 10}]}, "bar.py": {'
        + '"checksum": "efgh5678", "profile": [10, 0, 0, 0], "measurements": '
        + '[{"unit_name": "foo()", "start": {"line": 20, "column": 1}, '
        + '"end": {"line": 30, "column": 1}, "value": 10}]}}}}'
    )
    assert serializer.to_json() == expected


def test_all():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            [Measurement("bar()", Location(10, 1), Location(20, 1), 10)],
        )
    )
    codebase.add_file(
        SourceFileEntry(
            "bar.py",
            "efgh5678",
            [
                Measurement("foo()", Location(20, 1), Location(30, 1), 10),
                Measurement("spam()", Location(30, 1), Location(40, 1), 10),
            ],
        )
    )

    assert len(codebase.all_measurements()) == 3
