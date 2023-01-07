from dataclasses import dataclass

from codelimit.common.SourceMeasurement import SourceMeasurement


@dataclass
class ReportUnit:
    file: str
    measurement: SourceMeasurement
