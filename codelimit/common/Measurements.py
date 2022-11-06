import dataclasses
import json

from codelimit.common.Measurement import Measurement


class Measurements:
    def __init__(self):
        self._measurements = []

    def add(self, measurement: Measurement):
        self._measurements.append(measurement)

    def all(self) -> list[Measurement]:
        return self._measurements

    def total_loc(self) -> int:
        result = 0
        for m in self._measurements:
            result += m.length
        return result

    def sorted_by_length(self):
        return sorted(self._measurements, key=lambda m: m.length)

    def to_json(self, pretty_print=False) -> str:
        class EnhancedJSONEncoder(json.JSONEncoder):
            def default(self, o):
                if dataclasses.is_dataclass(o):
                    return dataclasses.asdict(o)
                return super().default(o)

        if pretty_print:
            return json.dumps(self._measurements, cls=EnhancedJSONEncoder, indent=2)
        else:
            return json.dumps(self._measurements, cls=EnhancedJSONEncoder)
