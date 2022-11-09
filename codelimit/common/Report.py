from math import floor, ceil

import plotext

from codelimit.common.Codebase import Codebase
from codelimit.common.utils import risk_categories


class Report:
    def __init__(self, measurements: Codebase):
        self.measurements = measurements

    def get_average(self):
        if len(self.measurements.all_measurements()) == 0:
            return 0
        return ceil(self.measurements.total_loc() / len(self.measurements.all_measurements()))

    def ninetieth_percentile(self):
        sorted_measurements = self.measurements.all_measurements_sorted_by_length()
        lines_of_code_90_percent = floor(self.measurements.total_loc() * 0.9)
        smallest_units_loc = 0
        for index, m in enumerate(sorted_measurements):
            smallest_units_loc += m.value
            if smallest_units_loc > lines_of_code_90_percent:
                return sorted_measurements[index].value
        return 0

    def risk_categories(self):
        return risk_categories(self.measurements.all_measurements())

    def display_risk_category_plot(self):
        labels = ["1-15", "16-30", "31-60", '60+']
        volume = risk_categories(self.measurements.all_measurements())
        plotext.title("Most Favored Pizzas in the World")
        plotext.simple_bar(labels, volume, color=[34, 226, 214, 196])
        plotext.show()
