from json import loads
from typing import Optional

from codelimit.common.Codebase import Codebase
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.report.Report import Report


class ReportReader:
    @staticmethod
    def from_json(json: str) -> Optional[Report]:
        d = loads(json)
        codebase = Codebase(d["root"])
        report = Report(codebase)
        report.version = d["version"] if "version" in d else None
        if report.version != Report.VERSION:
            return None
        report.uuid = d["uuid"]
        for k, v in d["codebase"]["files"].items():
            measurements: list[Measurement] = []
            for m in v["measurements"]:
                start_location = Location(m["start"]["line"], m["start"]["column"])
                end_location = Location(m["end"]["line"], m["end"]["column"])
                measurements.append(
                    Measurement(
                        m["unit_name"], start_location, end_location, m["value"]
                    )
                )
            codebase.add_file(
                SourceFileEntry(k, v["checksum"], v["language"], v["loc"], measurements)
            )
        codebase.aggregate()
        return report
