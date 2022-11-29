import json

from codelimit.common.SourceFolder import SourceFolder
from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.utils import EnhancedJSONEncoder, get_parent_folder, get_basename


class Codebase:
    def __init__(self):
        self.tree = {'.': SourceFolder()}
        self.measurements = {}

    def add_file(self, path: str, measurements: list[SourceMeasurement]):
        self.measurements[path] = measurements
        parent_folder = get_parent_folder(path)
        if parent_folder not in self.tree:
            self.add_folder(parent_folder)
        folder = self.tree[parent_folder]
        folder.add_file(get_basename(path))

    def add_folder(self, path: str):
        if path == '.':
            return
        if path not in self.tree:
            self.tree[path] = SourceFolder()
            self.add_folder(get_parent_folder(path))
        parent_folder = self.tree[get_parent_folder(path)]
        parent_folder.add_folder(get_basename(path))

    def all_files(self) -> list[str]:
        return list(self.measurements.keys())

    def all_measurements(self) -> list[SourceMeasurement]:
        result = []
        for m in self.measurements.values():
            result.extend(m)
        return result

    def all_measurements_sorted_by_length(self):
        return sorted(self.all_measurements(), key=lambda m: m.value)

    def total_loc(self) -> int:
        result = 0
        for m in self.all_measurements():
            result += m.value
        return result

    def to_json(self, pretty_print=False) -> str:
        if pretty_print:
            return json.dumps(self, cls=EnhancedJSONEncoder, indent=2)
        else:
            return json.dumps(self, cls=EnhancedJSONEncoder)
