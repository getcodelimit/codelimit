from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.utils import risk_categories


class SourceFile:
    def __init__(self, path: str, measurements: list[SourceMeasurement] = None):
        self.path = path
        if measurements:
            self.measurements = measurements
        else:
            self.measurements = []

    def risk_categories(self):
        return risk_categories(self.measurements)
