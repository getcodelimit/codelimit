from __future__ import annotations

from codelimit.common.SourceFolderEntry import SourceFolderEntry


class SourceFolder:
    def __init__(self):
        self.entries: list[SourceFolderEntry] = []

    def add_file(self, name: str):
        self.entries.append(SourceFolderEntry(name))

    def add_folder(self, name: str):
        self.entries.append(SourceFolderEntry(name))
