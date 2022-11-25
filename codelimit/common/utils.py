from typing import Union

from codelimit.common.SourceMeasurement import SourceMeasurement


def risk_categories(measurements: list[SourceMeasurement]):
    result = [0, 0, 0, 0]
    for m in measurements:
        if m.value <= 15:
            result[0] += m.value
        elif m.value <= 30:
            result[1] += m.value
        elif m.value <= 60:
            result[2] += m.value
        else:
            result[3] += m.value
    return result


def path_has_suffix(path: str, suffixes: Union[str, list[str]]):
    dot_index = path.rfind('.')
    if dot_index >= 0:
        suffix = path[dot_index + 1:]
        if type(suffixes) == list:
            return suffix in suffixes
        else:
            return suffix == suffixes
    else:
        return False
