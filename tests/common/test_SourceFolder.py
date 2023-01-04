from codelimit.common.SourceFolder import SourceFolder


def test_codebase_entry_multiple_files():
    folder = SourceFolder()

    folder.add_file('foo.py', [])
    folder.add_file('bar.py', [])

    assert folder.entries and len(folder.entries) == 2

    assert 'foo.py' in [e.name for e in folder.entries]
    assert 'bar.py' in [e.name for e in folder.entries]
