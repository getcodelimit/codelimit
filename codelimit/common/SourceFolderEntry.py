from typing import Union

from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.utils import risk_categories


class SourceFolderEntry:
    def __init__(self, name: str, measurements: list[SourceMeasurement] = None):
        self.name = name
        loc = sum([m.value for m in measurements]) if measurements else None
        self.loc: Union[int, None] = loc
        rc = risk_categories(measurements) if measurements else None
        self.risk_categories: Union[list[int], None] = rc
