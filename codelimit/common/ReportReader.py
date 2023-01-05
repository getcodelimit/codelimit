from json import loads

from codelimit.common.Codebase import Codebase
from codelimit.common.Report import Report
from codelimit.common.SourceMeasurement import SourceMeasurement


class ReportReader:

    @staticmethod
    def from_json(json: str) -> Report:
        d = loads(json)
        codebase = Codebase()
        report = Report(codebase)
        report.uuid = d['uuid']
        for k, v in d['codebase']['measurements'].items():
            measurements: list[SourceMeasurement] = []
            for m in v:
                measurements.append(SourceMeasurement(m['start_line'], m['value']))
            codebase.add_file(k, measurements)
        return report
