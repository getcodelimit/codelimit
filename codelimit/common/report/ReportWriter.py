from codelimit.common.CodebseEntry import CodebaseEntry
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.SourceFolder import SourceFolder
from codelimit.common.report.Report import Report


class ReportWriter:
    def __init__(self, report: Report, pretty_print=True):
        self.report = report
        self.tree = report.codebase.tree
        self.files = report.codebase.files
        self.pretty_print = pretty_print
        self.level = 0

    def to_json(self) -> str:
        self.level = 0
        json = ""
        json += self._open("{")
        json += self._collection(
            [
                self._line(f'"uuid": "{self.report.uuid}"'),
                self._line(f'"root": "{self.report.codebase.root}"'),
                self._codebase_to_json(),
            ]
        )
        json += self._close("}")
        return json

    def _open(self, text: str) -> str:
        json = self._line(text)
        self.level += 2
        return json

    def _close(self, text: str) -> str:
        self.level -= 2
        return self._line(text)

    def _line(self, text: str) -> str:
        if self.pretty_print:
            return (self.level * " ") + f"{text}\n"
        else:
            return text

    def _collection(self, items: list):
        separator = ",\n" if self.pretty_print else ", "
        json = separator.join([i.rstrip() for i in items])
        return json + "\n" if self.pretty_print and len(items) > 0 else json

    def _codebase_to_json(self):
        json = ""
        json += self._open('"codebase": {')
        json += self._collection([self._tree_to_json(), self._measurements_to_json()])
        json += self._close("}")
        return json

    def _tree_to_json(self):
        json = ""
        json += self._open('"tree": {')
        json += self._collection(
            [self._tree_item_to_json(k, v) for k, v in self.tree.items()]
        )
        json += self._close("}")
        return json

    def _tree_item_to_json(self, name: str, folder: SourceFolder) -> str:
        json = ""
        json += self._open(f'"{name}": {{')
        json += self._collection(
            [
                self._tree_item_entries_to_json(folder),
                self._tree_item_profile_to_json(name),
            ]
        )
        json += self._close("}")
        return json

    def _tree_item_entries_to_json(self, folder: SourceFolder):
        json = ""
        json += self._open('"entries": [')
        json += self._collection(
            [self._source_folder_entry_to_json(f) for f in folder.entries]
        )
        json += self._close("]")
        return json

    def _tree_item_profile_to_json(self, name: str):
        return self._line(f'"profile": {self.tree[name].profile}')

    def _measurements_to_json(self):
        json = ""
        json += self._open('"files": {')
        json += self._collection(
            [self._file_to_json(k, v) for k, v in self.files.items()]
        )
        json += self._close("}")
        return json

    def _file_to_json(self, name: str, entry: SourceFileEntry):
        json = ""
        json += self._open(f'"{name}": {{')
        json += self._collection(
            [
                self._file_checksum_to_json(entry),
                self._file_profile_to_json(entry),
                self._file_measurements_to_json(entry),
            ]
        )
        json += self._close("}")
        return json

    def _file_checksum_to_json(self, entry: SourceFileEntry):
        return self._line(f'"checksum": "{entry.checksum()}"')

    def _file_profile_to_json(self, entry: SourceFileEntry):
        return self._line(f'"profile": {entry.profile()}')

    def _file_measurements_to_json(self, entry: SourceFileEntry):
        json = ""
        json += self._open('"measurements": [')
        json += self._collection(
            [self._measurement_to_json(m) for m in entry.measurements()]
        )
        json += self._close("]")
        return json

    def _measurement_to_json(self, measurement: Measurement) -> str:
        json = ""
        json += f'{{"unit_name": "{measurement.unit_name}", '
        json += (
            f'"start": {{"line": {measurement.start.line}, "column": '
            f"{measurement.start.column}}}, "
        )
        json += (
            f'"end": {{"line": {measurement.end.line}, "'
            f'column": {measurement.end.column}}}, '
        )
        json += f'"value": {measurement.value}}}'
        return self._line(json)

    def _source_folder_entry_to_json(self, entry: CodebaseEntry) -> str:
        return self._line(f'"{entry.name}"')
