from dataclasses import dataclass


@dataclass
class SourceMeasurement:
    unit_name: str
    start_line: int
    value: int
