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
        for file, entry in self.codebase.files.items():
            for m in entry.measurements():
                result.append(ReportUnit(file, m))
        result = sorted(result, key=lambda unit: unit.measurement.value, reverse=True)
        return result

    def quality_profile(self):
        return make_profile(self.codebase.all_measurements())

    def summary(self) -> str:
        medium_risk = len(
            [m for m in self.codebase.all_measurements() if 30 < m.value <= 60]
        )
        high_risk = len([m for m in self.codebase.all_measurements() if m.value > 60])
        if high_risk > 0:
            return f"Refactoring necessary: 🚨 Unmaintainable functions: {high_risk}"
        elif medium_risk > 0:
            return (
                f"Refactoring necessary: 🔔 Hard to maintain functions: "
                f"{medium_risk}"
            )
        else:
            return "Refactoring not necessary, happy coding!"

    def risk_category_plot(self) -> str:
        def get_labels(profile):
            labels = ["1-15"]
            if profile[1] > 0:
                labels.append("16-30")
            if profile[2] > 0:
                labels.append("31-60")
            if profile[3] > 0:
                labels.append("60+")
            return labels

        profile = make_profile(self.codebase.all_measurements())
        plot_labels = get_labels(profile)
        plotext.simple_stacked_bar(
            [""],
            [[profile[0]], [profile[1]], [profile[2]], [profile[3]]],
            width=100,
            labels=plot_labels,
            colors=[34, 226, 214, 196],
        )
        result = plotext.build()
        total_loc = sum(profile)
        result = result.replace(f"\x1b[1m\x1b[38;5;7m{total_loc}.0\x1b[0m\x1b[0m", "")
        return result
