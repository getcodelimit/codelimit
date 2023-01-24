from math import floor, ceil
from uuid import uuid4

import plotext

from codelimit.common.Codebase import Codebase
from codelimit.common.report.ReportUnit import ReportUnit
from codelimit.common.utils import make_profile


class Report:
    def __init__(self, codebase: Codebase):
        self.uuid = str(uuid4())
        self.codebase = codebase

    def get_average(self):
        if len(self.codebase.all_measurements()) == 0:
            return 0
        return ceil(self.codebase.total_loc() / len(self.codebase.all_measurements()))

    def ninetieth_percentile(self):
        sorted_measurements = self.codebase.all_measurements_sorted_by_length_asc()
        lines_of_code_90_percent = floor(self.codebase.total_loc() * 0.9)
        smallest_units_loc = 0
        for index, m in enumerate(sorted_measurements):
            smallest_units_loc += m.value
            if smallest_units_loc > lines_of_code_90_percent:
                return sorted_measurements[index].value
        return 0

    def all_report_units_sorted_by_length_asc(self) -> list[ReportUnit]:
        result = []
        for file, measurements in self.codebase.measurements.items():
            for m in measurements:
                result.append(ReportUnit(file, m))
        result = sorted(result, key=lambda unit: unit.measurement.value, reverse=True)
        return result

    def risk_categories(self):
        return make_profile(self.codebase.all_measurements())

    def display_risk_category_plot(self):
        labels = ["1-15", "16-30", "31-60", '60+']
        volume = make_profile(self.codebase.all_measurements())
        plotext.simple_stacked_bar([''], [[volume[0]], [volume[1]], [volume[2]], [volume[3]]], width=100, labels=labels,
                                   colors=[34, 226, 214, 196]);
        plotext.show()
