from dataclasses import dataclass


@dataclass
class SourceMeasurement:
    start_line: int
    value: int
