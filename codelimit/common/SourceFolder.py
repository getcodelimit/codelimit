from __future__ import annotations

from codelimit.common.SourceFolderEntry import SourceFolderEntry
from codelimit.common.SourceMeasurement import SourceMeasurement


class SourceFolder:
    def __init__(self):
        self.entries: list[SourceFolderEntry] = []

    def add_file(self, name: str, measurements: list[SourceMeasurement]):
        self.entries.append(SourceFolderEntry(name, measurements))

    def add_folder(self, name: str):
        self.entries.append(SourceFolderEntry(name))
