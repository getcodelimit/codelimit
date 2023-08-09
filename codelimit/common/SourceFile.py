from typing import Union

from codelimit.common.Measurement import Measurement


class SourceFile:
    def __init__(self, path: str, measurements: Union[list[Measurement], None] = None):
        self.path = path
        if measurements:
            self.measurements = measurements
        else:
            self.measurements = []
