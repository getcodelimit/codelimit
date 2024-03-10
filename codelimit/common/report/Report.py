from math import floor, ceil
from uuid import uuid4

from codelimit.common.Codebase import Codebase
from codelimit.common.report.ReportUnit import ReportUnit
from codelimit.common.utils import make_profile


class Report:
    VERSION = "1.0"

    def __init__(self, codebase: Codebase):
        self.version = self.VERSION
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

    def all_report_units_sorted_by_length_asc(self, threshold=0) -> list[ReportUnit]:
        result = []
        for file, entry in self.codebase.files.items():
            for m in entry.measurements():
                if m.value > threshold:
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
            return f"🚨 Refactoring necessary, unmaintainable functions: {high_risk}"
        elif medium_risk > 0:
            return (
                f"🔔 Don't forget to refactor, hard-to-maintain functions: "
                f"{medium_risk}"
            )
        else:
            return "Refactoring not necessary, happy coding!"
