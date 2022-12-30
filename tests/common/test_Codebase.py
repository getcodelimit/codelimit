from codelimit.common.Codebase import Codebase
from codelimit.common.Report import Report
from codelimit.common.ReportSerializer import ReportSerializer
from codelimit.common.SourceFolder import SourceFolder


def test_codebase_empty():
    codebase = Codebase()
    tree_keys = list(codebase.tree.keys())

    assert len(tree_keys) == 1
    assert tree_keys[0] == '.'


def test_codebase_entry_single_file():
    codebase = Codebase()
    codebase.add_file('foo.py', [])
    report = Report(codebase)
    serializer = ReportSerializer(report, False)

    assert serializer.to_json() == \
           '{"uuid": "' + report.uuid + '", "codebase": {"tree": {".": {"entries": [{"name": "foo.py"}]}}, "measurements": {"foo.py": []}}}'


def test_codebase_entry_single_folder_single_file():
    codebase = Codebase()
    codebase.add_file('foo/bar.py', [])
    report = Report(codebase)
    serializer = ReportSerializer(report, False)

    assert serializer.to_json() == '{"uuid": "' + report.uuid + '", "codebase": {"tree": {".": {"entries": [{"name": "foo"}]}, ' + \
           '"foo": {"entries": [{"name": "bar.py"}]}}, "measurements": {"foo/bar.py": []}}}'


def test_codebase_entry_multple_files():
    folder = SourceFolder()

    folder.add_file('bar.py', [])
    folder.add_folder('spam')

    assert folder.entries and len(folder.entries) == 2

    assert 'bar.py' in [e.name for e in folder.entries]
    assert 'spam' in [e.name for e in folder.entries]
