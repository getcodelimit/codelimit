from dataclasses import dataclass
from math import floor, ceil


@dataclass
class Measurement:
    filename: str
    line: int
    length: int


class Report:
    def __init__(self):
        self.measurements: list[Measurement] = []
        self.total_lines_of_code = 0

    def add_measurement(self, measurement: Measurement):
        self.measurements.append(measurement)
        self.total_lines_of_code += measurement.length

    def get_average(self):
        return ceil(self.total_lines_of_code / len(self.measurements))

    def ninetieth_percentile(self):
        self.measurements.sort(key=lambda m: m.length)
        lines_of_code_90_percent = floor(self.total_lines_of_code * 0.1)
        smallest_units_loc = 0
        for index, m in enumerate(self.measurements):
            smallest_units_loc += m.length
            if smallest_units_loc > lines_of_code_90_percent:
                return self.measurements[index].length

    def display(self):
        for m in self.measurements:
            print(f'{m.filename}#{m.line}: {m.length}')
