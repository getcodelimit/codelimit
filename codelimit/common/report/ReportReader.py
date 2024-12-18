from json import loads
from typing import Optional

from codelimit.common.Codebase import Codebase
from codelimit.common.GithubRepository import GithubRepository
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.report.Report import Report


class ReportReader:
    @staticmethod
    def get_report_version(json: str) -> Optional[str]:
        d = loads(json)
        return d["version"] if "version" in d else None

    @staticmethod
    def from_json(json: str) -> Report:
        d = loads(json)
        codebase = Codebase(d["root"])
        if 'repository' in d:
            repository = GithubRepository(**d["repository"])
            report = Report(codebase, repository)
        else:
            report = Report(codebase)
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
