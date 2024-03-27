from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.SourceFolder import SourceFolder


def test_codebase_entry_multiple_files():
    folder = SourceFolder()

    folder.add_file(SourceFileEntry("foo.py", "abcd1234", "Python", 0, []))
    folder.add_file(SourceFileEntry("bar.py", "efgh5678", "Python", 0, []))

    assert folder.entries and len(folder.entries) == 2

    assert "foo.py" in [e.name for e in folder.entries]
    assert "bar.py" in [e.name for e in folder.entries]
