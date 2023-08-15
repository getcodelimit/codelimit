from dataclasses import dataclass

from codelimit.common.Measurement import Measurement


@dataclass
class ReportUnit:
    file: str
    measurement: Measurement
