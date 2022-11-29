import dataclasses
import json
import os
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


def get_parent_folder(path: str) -> Union[str, None]:
    parts = path.split(os.path.sep)
    if len(parts) == 1:
        return '.'
    else:
        return os.path.sep.join(parts[0:-1])


def get_basename(path: str) -> str:
    parts = path.split(os.path.sep)
    return parts[-1]


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        def include(value):
            if value is None:
                return False
            if isinstance(value, list):
                return len(value) > 0
            return True

        if dataclasses.is_dataclass(o):
            return dict((key, value) for key, value in dataclasses.asdict(o).items() if include(value))
        else:
            return dict((key, value) for key, value in o.__dict__.items() if include(value))
