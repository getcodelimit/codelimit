import json

from codelimit.common.SourceFile import SourceFile
from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.utils import EnhancedJSONEncoder


class Codebase:
    def __init__(self):
        self.files: list[SourceFile] = []

    def add(self, file: SourceFile):
        self.files.append(file)

    def all_file_measurements(self):
        return self.files

    def all_measurements(self) -> list[SourceMeasurement]:
        result = []
        for f in self.files:
            result.extend(f.measurements)
        return result

    def all_measurements_sorted_by_length(self):
        return sorted(self.all_measurements(), key=lambda m: m.value)

    def total_loc(self) -> int:
        result = 0
        for file in self.files:
            for m in file.measurements:
                result += m.value
        return result

    def to_json(self, pretty_print=False) -> str:
        if pretty_print:
            return json.dumps(self.files, cls=EnhancedJSONEncoder, indent=2)
        else:
            return json.dumps(self.files, cls=EnhancedJSONEncoder)
