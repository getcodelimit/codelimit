from dataclasses import dataclass

from codelimit.common.SourceMeasurement import SourceMeasurement


@dataclass
class ReportUnit:
    file: str
    measurement: SourceMeasurement


def format_report_unit(unit: ReportUnit) -> str:
    name = unit.measurement.unit_name
    length = unit.measurement.value
    prefix = f'[{length:3}]' if length < 61 else '[60+]'
    return f'{prefix} {name}'
