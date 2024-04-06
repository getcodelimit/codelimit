from __future__ import annotations

from codelimit.common.CodebseEntry import CodebaseEntry
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.SourceFolderEntry import SourceFolderEntry


class SourceFolder:
    def __init__(self) -> None:
        self.entries: list[CodebaseEntry] = []
        self.profile = [0, 0, 0, 0]

    def add_file(self, entry: SourceFileEntry):
        self.entries.append(entry)

    def add_folder(self, name: str):
        self.entries.append(SourceFolderEntry(f"{name}"))
