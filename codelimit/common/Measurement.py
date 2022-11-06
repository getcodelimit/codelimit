from dataclasses import dataclass


@dataclass
class Measurement:
    filename: str
    line: int
    length: int
