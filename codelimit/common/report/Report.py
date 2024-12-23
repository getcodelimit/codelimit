from datetime import datetime, timezone
from math import floor, ceil
from uuid import uuid4

from codelimit.common.Codebase import Codebase
from codelimit.common.GithubRepository import GithubRepository
from codelimit.common.report.ReportUnit import ReportUnit
from codelimit.common.utils import make_profile
from codelimit.version import version


class Report:
    VERSION = version

    def __init__(self, codebase: Codebase, repository: GithubRepository | None = None):
        self.version: str | None = self.VERSION
        self.uuid = str(uuid4())
        self.timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
        self.repository = repository
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

    def quality_profile_percentage(self):
        profile = self.quality_profile()
        total = sum(profile)
        unmaintainable = ceil((profile[3] / total) * 100) if total > 0 else 0
        hard_to_maintain = ceil((profile[2] / total) * 100) if total > 0 else 0
        verbose = ceil((profile[1] / total) * 100) if total > 0 else 0
        easy = 100 - unmaintainable - hard_to_maintain - verbose
        return easy, verbose, hard_to_maintain, unmaintainable
