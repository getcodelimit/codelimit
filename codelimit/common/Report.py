import json
from math import floor, ceil
from uuid import uuid4

import plotext

from codelimit.common.Codebase import Codebase
from codelimit.common.utils import risk_categories, EnhancedJSONEncoder


class Report:
    def __init__(self, codebase: Codebase):
        self.uuid = str(uuid4())
        self.codebase = codebase

    def get_average(self):
        if len(self.codebase.all_measurements()) == 0:
            return 0
        return ceil(self.codebase.total_loc() / len(self.codebase.all_measurements()))

    def ninetieth_percentile(self):
        sorted_measurements = self.codebase.all_measurements_sorted_by_length()
        lines_of_code_90_percent = floor(self.codebase.total_loc() * 0.9)
        smallest_units_loc = 0
        for index, m in enumerate(sorted_measurements):
            smallest_units_loc += m.value
            if smallest_units_loc > lines_of_code_90_percent:
                return sorted_measurements[index].value
        return 0

    def risk_categories(self):
        return risk_categories(self.codebase.all_measurements())

    def display_risk_category_plot(self):
        labels = ["1-15", "16-30", "31-60", '60+']
        volume = risk_categories(self.codebase.all_measurements())
        plotext.title("Most Favored Pizzas in the World")
        plotext.simple_bar(labels, volume, color=[34, 226, 214, 196])
        plotext.show()

    def to_json(self, pretty_print=False) -> str:
        if pretty_print:
            return json.dumps(self, cls=EnhancedJSONEncoder, indent=2)
        else:
            return json.dumps(self, cls=EnhancedJSONEncoder)
