from codelimit.common.Codebase import Codebase
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportWriter import ReportWriter


def test_codebase_empty():
    codebase = Codebase("/")
    tree_keys = list(codebase.tree.keys())

    assert len(tree_keys) == 1
    assert tree_keys[0] == "./"


def test_codebase_entry_single_file():
    codebase = Codebase("/")
    codebase.add_file(SourceFileEntry("foo.py", "abcd1234", "Python", 20, []))
    report = Report(codebase)
    writer = ReportWriter(report, False)

    assert (
            writer.to_json()
            == f'{{"version": "{report.version}", "uuid": "{report.uuid}", '
               f'"timestamp": "{report.timestamp}", '
               '"root": "/", "codebase": {"totals": {"Python": {"files": 1, "lines_of_code": '
               '20, "functions": 0, "hard_to_maintain": 0, "unmaintainable": 0}}, "tree": '
               '{"./": {"entries": ["foo.py"], "profile": [0, 0, 0, 0]}}, "files": '
               '{"foo.py": {"checksum": "abcd1234", "language": "Python", "loc": 20, '
               '"profile": [0, 0, 0, 0], "measurements": []}}}}'
    )


def test_codebase_entry_single_folder_single_file():
    codebase = Codebase("/")
    codebase.add_file(SourceFileEntry("foo/bar.py", "abcd1234", "Python", 20, []))
    report = Report(codebase)
    writer = ReportWriter(report, False)

    assert (
            writer.to_json()
            == f'{{"version": "{report.version}", "uuid": "{report.uuid}", '
               f'"timestamp": "{report.timestamp}", '
               '"root": "/", "codebase": {"totals": {"Python": {"files": 1, "lines_of_code": '
               '20, "functions": 0, "hard_to_maintain": 0, "unmaintainable": 0}}, "tree": '
               '{"./": {"entries": ["foo/"], "profile": [0, 0, 0, 0]}, "foo/": {"entries": '
               '["bar.py"], "profile": [0, 0, 0, 0]}}, "files": {"foo/bar.py": {"checksum": '
               '"abcd1234", "language": "Python", "loc": 20, "profile": [0, 0, 0, 0], '
               '"measurements": []}}}}'
    )


def test_codebase_multiple_files():
    codebase = Codebase("/")
    codebase.add_file(SourceFileEntry("foo.py", "abcd1234", "Python", 20, []))
    codebase.add_file(SourceFileEntry("bar.py", "efgh5678", "Python", 20, []))

    assert len(codebase.tree["./"].entries) == 2


def test_codebase_multiple_folders():
    codebase = Codebase("/")
    codebase.add_folder("foo")
    codebase.add_folder("foo/spam")

    assert len(codebase.tree["./"].entries) == 1
    assert len(codebase.tree["foo/"].entries) == 1
    assert len(codebase.tree["foo/spam/"].entries) == 0


def test_codebase_multiple_files_and_folders():
    codebase = Codebase("/")
    codebase.add_folder("foo")
    codebase.add_file(SourceFileEntry("foo/bar.py", "abcd1234", "Python", 20, []))
    codebase.add_folder("foo/spam")
    codebase.add_file(SourceFileEntry("foo/spam/bar.py", "efgh5678", "Python", 20, []))

    assert len(codebase.tree["./"].entries) == 1
    assert len(codebase.tree["foo/"].entries) == 2
    assert len(codebase.tree["foo/spam/"].entries) == 1


def test_codebase_aggregate():
    codebase = Codebase("/")
    codebase.add_folder("foo")
    codebase.add_file(
        SourceFileEntry(
            "foo/bar.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("bar()", Location(1, 1), Location(10, 1), 10)],
        )
    )
    codebase.add_folder("foo/spam")
    codebase.add_file(
        SourceFileEntry(
            "foo/spam/bar.py",
            "efgh5678",
            "Python",
            20,
            [Measurement("spam()", Location(1, 1), Location(10, 1), 20)],
        )
    )

    codebase.aggregate()

    assert codebase.tree["foo/spam/"].profile == [0, 20, 0, 0]
