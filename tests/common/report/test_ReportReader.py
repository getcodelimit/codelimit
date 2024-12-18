from codelimit.common.Codebase import Codebase
from codelimit.common.GithubRepository import GithubRepository
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter


def test_empty_report():
    codebase = Codebase("/")
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.uuid == report.uuid

    result_entries = result.codebase.tree["./"].entries
    result_measurements = result.codebase.files

    assert len(result_entries) == 0
    assert len(result_measurements) == 0


def test_from_json():
    json = ""
    json += "{"
    json += f'  "version": "{Report.VERSION}",'
    json += '  "uuid": "abcdefgh",'
    json += '  "root": "/tmp",'
    json += '  "codebase": {'
    json += '    "totals": {},'
    json += '    "tree": {'
    json += '       "./": {'
    json += '         "entries": [],'
    json += '         "profile": [0, 0, 0, 0]'
    json += "       }"
    json += "    },"
    json += '    "files": {}'
    json += "  }"
    json += "}"

    result = ReportReader.from_json(json)

    assert result.version == Report.VERSION
    assert result.uuid == "abcdefgh"
    assert result.codebase.root == "/tmp"


def test_version():
    json = ""
    json += "{"
    json += f'  "version": "{Report.VERSION}",'
    json += '  "uuid": "a417ac45-973e-44f8-aa98-f6a29844caf1",'
    json += '  "root": "/",'
    json += '  "codebase": {'
    json += '    "tree": {'
    json += '       "./": {'
    json += '         "entries": [],'
    json += '         "profile": [0, 0, 0, 0]'
    json += "       }"
    json += "    },"
    json += '    "files": {}'
    json += "  }"
    json += "}"

    result = ReportReader.get_report_version(json)

    assert result == Report.VERSION


def test_no_version():
    json = ""
    json += "{"
    json += '  "uuid": "a417ac45-973e-44f8-aa98-f6a29844caf1",'
    json += '  "root": "/",'
    json += '  "codebase": {'
    json += '    "tree": {'
    json += '       "./": {'
    json += '         "entries": [],'
    json += '         "profile": [0, 0, 0, 0]'
    json += "       }"
    json += "    },"
    json += '    "files": {}'
    json += "  }"
    json += "}"

    result = ReportReader.get_report_version(json)

    assert result is None


def test_single_file():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("bar()", Location(10, 1), Location(30, 1), 20)],
        )
    )
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.uuid == report.uuid

    assert len(result.codebase.totals) == 1
    assert result.codebase.totals["Python"].loc == 20

    result_entries = result.codebase.tree["./"].entries
    result_measurements = result.codebase.files

    assert len(result_entries) == 1
    assert result_entries[0].is_file()
    assert result_entries[0].name == "foo.py"
    assert len(result_measurements) == 1

    foo_measurements = result_measurements["foo.py"].measurements()

    assert len(foo_measurements) == 1
    assert foo_measurements[0].start.line == 10
    assert foo_measurements[0].value == 20


def test_profile():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("bar()", Location(10, 1), Location(30, 1), 20)],
        )
    )
    codebase.aggregate()
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.codebase.tree["./"].profile == [0, 20, 0, 0]

def test_repository():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("bar()", Location(10, 1), Location(30, 1), 20)],
        )
    )
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.repository is None

    report = Report(codebase, GithubRepository("getcodelimit", "codelimit", branch="main"))

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.repository is not None
    assert result.repository.owner == "getcodelimit"
    assert result.repository.name == "codelimit"
    assert result.repository.branch == "main"



def test_multiple_files():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("spam()", Location(10, 1), Location(30, 1), 20)],
        )
    )
    codebase.add_file(
        SourceFileEntry(
            "bar.py",
            "efgh5678",
            "Python",
            20,
            [
                Measurement("eggs()", Location(10, 1), Location(30, 1), 20),
                Measurement("ham()", Location(20, 1), Location(50, 1), 30),
            ],
        )
    )
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.uuid == report.uuid

    result_entries = result.codebase.tree["./"].entries
    result_files = result.codebase.files

    assert len(result_entries) == 2
    assert result_entries[0].is_file()
    assert result_entries[0].name == "foo.py"
    assert result_entries[1].is_file()
    assert result_entries[1].name == "bar.py"
    assert len(result_files) == 2
    assert len(result_files["foo.py"].measurements()) == 1
    assert len(result_files["bar.py"].measurements()) == 2

    bar_measurements = result_files["bar.py"].measurements()

    assert bar_measurements[1].start.line == 20
    assert bar_measurements[1].value == 30


def test_multiple_files_and_folders():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("bar()", Location(10, 1), Location(30, 1), 20)],
        )
    )
    codebase.add_file(
        SourceFileEntry(
            "bar/spam.py",
            "efgh5678",
            "Python",
            20,
            [
                Measurement("spam()", Location(10, 1), Location(30, 1), 20),
                Measurement("eggs()", Location(20, 1), Location(50, 1), 30),
            ],
        )
    )
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.uuid == report.uuid

    result_entries = result.codebase.tree["./"].entries

    assert len(result_entries) == 2
    assert result_entries[0].is_file()
    assert result_entries[0].name == "foo.py"
    assert result_entries[1].name == "bar/"
    assert result_entries[1].is_folder()

    result_entries = result.codebase.tree["bar/"].entries

    assert len(result_entries) == 1
    assert result_entries[0].is_file()
    assert result_entries[0].name == "spam.py"

    result_files = result.codebase.files

    assert len(result_files) == 2
    assert len(result_files["foo.py"].measurements()) == 1
    assert len(result_files["bar/spam.py"].measurements()) == 2

    bar_measurements = result_files["bar/spam.py"].measurements()

    assert bar_measurements[1].start.line == 20
    assert bar_measurements[1].value == 30
