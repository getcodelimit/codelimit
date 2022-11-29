from codelimit.common.Codebase import Codebase
from codelimit.common.SourceFolder import SourceFolder


def test_codebase_empty():
    codebase = Codebase()
    tree_keys = list(codebase.tree.keys())

    assert len(tree_keys) == 1
    assert tree_keys[0] == '.'


def test_codebase_entry_single_file():
    codebase = Codebase()
    codebase.add_file('foo.py', [])

    assert codebase.to_json(
        False) == '{"tree": {".": {"entries": [{"name": "foo.py"}]}}, "measurements": {"foo.py": []}}'


def test_codebase_entry_multple_files():
    folder = SourceFolder()

    folder.add_file('bar.py')
    folder.add_folder('spam')

    assert folder.entries and len(folder.entries) == 2

    assert 'bar.py' in [e.name for e in folder.entries]
    assert 'spam' in [e.name for e in folder.entries]
