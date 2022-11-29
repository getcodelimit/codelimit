from codelimit.common.SourceMeasurement import SourceMeasurement


class SourceFile:
    def __init__(self, path: str, measurements: list[SourceMeasurement] = None):
        self.path = path
        if measurements:
            self.measurements = measurements
        else:
            self.measurements = []
