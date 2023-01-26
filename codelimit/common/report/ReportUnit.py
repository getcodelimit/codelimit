from dataclasses import dataclass

from codelimit.common.SourceMeasurement import SourceMeasurement


@dataclass
class ReportUnit:
    file: str
    measurement: SourceMeasurement


def format_report_unit(unit: ReportUnit) -> str:
    name = unit.measurement.unit_name
    length = unit.measurement.value
    if length > 60:
        circle = '🔴'
    elif length > 30:
        circle = '🟠'
    elif length > 15:
        circle = '🟡'
    else:
        circle = '🟢'
    prefix = f'{circle} [{length:3}]' if length < 61 else f'{circle} [60+]'
    return f'{prefix} {name}'
