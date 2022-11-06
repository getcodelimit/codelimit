from dataclasses import dataclass
from math import floor, ceil

import plotext


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
        lines_of_code_90_percent = floor(self.total_lines_of_code * 0.9)
        smallest_units_loc = 0
        for index, m in enumerate(self.measurements):
            smallest_units_loc += m.length
            if smallest_units_loc > lines_of_code_90_percent:
                return self.measurements[index].length

    def risk_categories(self):
        result = [0, 0, 0, 0]
        for m in self.measurements:
            if m.length <= 10:
                result[0] += m.length
            elif m.length <= 20:
                result[1] += m.length
            elif m.length <= 30:
                result[2] += m.length
            else:
                result[3] += m.length
        return result

    def display_risk_category_plot(self):
        labels = ["1-10", "11-20", "21-30", '30+']
        volume = self.risk_categories()
        plotext.title("Most Favored Pizzas in the World")
        plotext.simple_bar(labels, volume, color=[34, 226, 214, 196])
        plotext.show()

    def display(self):
        for m in self.measurements:
            print(f'{m.filename}#{m.line}: {m.length}')
