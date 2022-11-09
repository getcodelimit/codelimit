import dataclasses
import json

from codelimit.common.SourceFile import SourceFile
from codelimit.common.SourceMeasurement import SourceMeasurement


class Codebase:
    def __init__(self):
        self._file_measurements = []

    def add(self, measurement: SourceFile):
        self._file_measurements.append(measurement)

    def all_file_measurements(self):
        return self._file_measurements

    def all_measurements(self) -> list[SourceMeasurement]:
        result = []
        for f in self._file_measurements:
            result.extend(f.measurements)
        return result

    def all_measurements_sorted_by_length(self):
        return sorted(self.all_measurements(), key=lambda m: m.value)

    def total_loc(self) -> int:
        result = 0
        for file_measurements in self._file_measurements:
            for m in file_measurements.measurements:
                result += m.value
        return result

    def to_json(self, pretty_print=False) -> str:
        class EnhancedJSONEncoder(json.JSONEncoder):
            def default(self, o):
                if dataclasses.is_dataclass(o):
                    return dataclasses.asdict(o)
                else:
                    return o.__dict__

        if pretty_print:
            return json.dumps(self._file_measurements, cls=EnhancedJSONEncoder, indent=2)
        else:
            return json.dumps(self._file_measurements, cls=EnhancedJSONEncoder)
