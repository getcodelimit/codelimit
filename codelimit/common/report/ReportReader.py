from json import loads

from codelimit.common.Codebase import Codebase
from codelimit.common.SourceLocation import SourceLocation
from codelimit.common.report.Report import Report
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
                start_location = SourceLocation(m['start']['line'], m['start']['column'])
                end_location = SourceLocation(m['end']['line'], m['end']['column'])
                measurements.append(SourceMeasurement(m['unit_name'], start_location, end_location, m['value']))
            codebase.add_file(k, measurements)
        return report
