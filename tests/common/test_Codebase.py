from codelimit.common.Codebase import Codebase
from codelimit.common.Report import Report
from codelimit.common.ReportSerializer import ReportSerializer
from codelimit.common.SourceMeasurement import SourceMeasurement


def test_codebase_empty():
    codebase = Codebase()
    tree_keys = list(codebase.tree.keys())

    assert len(tree_keys) == 1
    assert tree_keys[0] == './'


def test_codebase_entry_single_file():
    codebase = Codebase()
    codebase.add_file('foo.py', [])
    report = Report(codebase)
    serializer = ReportSerializer(report, False)

    assert serializer.to_json() == \
           '{"uuid": "' + report.uuid + '", "codebase": {"tree": {"./": {"entries": [{"name": "foo.py"}], "profile": [0, 0, 0, 0]}}, "measurements": {"foo.py": []}}}'


def test_codebase_entry_single_folder_single_file():
    codebase = Codebase()
    codebase.add_file('foo/bar.py', [])
    report = Report(codebase)
    serializer = ReportSerializer(report, False)

    assert serializer.to_json() == '{"uuid": "' + report.uuid + '", "codebase": {"tree": {"./": {"entries": [{"name": "foo/"}], "profile": [0, 0, 0, 0]}, ' + \
           '"foo/": {"entries": [{"name": "bar.py"}], "profile": [0, 0, 0, 0]}}, "measurements": {"foo/bar.py": []}}}'


def test_codebase_multiple_files():
    codebase = Codebase()
    codebase.add_file('foo.py', [])
    codebase.add_file('bar.py', [])

    assert len(codebase.tree['./'].entries) == 2


def test_codebase_multiple_folders():
    codebase = Codebase()
    codebase.add_folder('foo')
    codebase.add_folder('foo/spam')

    assert len(codebase.tree['./'].entries) == 1
    assert len(codebase.tree['foo/'].entries) == 1
    assert len(codebase.tree['foo/spam/'].entries) == 0


def test_codebase_multiple_files_and_folders():
    codebase = Codebase()
    codebase.add_folder('foo')
    codebase.add_file('foo/bar.py', [])
    codebase.add_folder('foo/spam')
    codebase.add_file('foo/spam/bar.py', [])

    assert len(codebase.tree['./'].entries) == 1
    assert len(codebase.tree['foo/'].entries) == 2
    assert len(codebase.tree['foo/spam/'].entries) == 1


def test_codebase_aggregate():
    codebase = Codebase()
    codebase.add_folder('foo')
    codebase.add_file('foo/bar.py', [SourceMeasurement(1, 10)])
    codebase.add_folder('foo/spam')
    codebase.add_file('foo/spam/bar.py', [SourceMeasurement(1, 20)])

    codebase.aggregate()

    assert codebase.tree['foo/spam/'].profile == [0, 20, 0, 0]
    print(codebase.tree['foo/'].profile)
