from dataclasses import dataclass

from codelimit.common.SourceLocation import SourceLocation


@dataclass
class SourceMeasurement:
    unit_name: str
    start: SourceLocation
    end: SourceLocation
    value: int
