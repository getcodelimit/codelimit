from math import floor, ceil

import plotext

from codelimit.common.Measurements import Measurements


class Report:
    def __init__(self, measurements: Measurements):
        self.measurements = measurements

    def get_average(self):
        if len(self.measurements.all()) == 0:
            return 0
        return ceil(self.measurements.total_loc() / len(self.measurements.all()))

    def ninetieth_percentile(self):
        sorted_measurements = self.measurements.sorted_by_length()
        lines_of_code_90_percent = floor(self.measurements.total_loc() * 0.9)
        smallest_units_loc = 0
        for index, m in enumerate(sorted_measurements):
            smallest_units_loc += m.length
            if smallest_units_loc > lines_of_code_90_percent:
                return sorted_measurements[index].length
        return 0

    def risk_categories(self):
        result = [0, 0, 0, 0]
        for m in self.measurements.all():
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
