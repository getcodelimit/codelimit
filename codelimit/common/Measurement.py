from dataclasses import dataclass

from codelimit.common.Location import Location


@dataclass
class Measurement:
    unit_name: str
    start: Location
    end: Location
    value: int
