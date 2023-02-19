from codelimit.common.Measurement import Measurement


class SourceFile:
    def __init__(self, path: str, measurements: list[Measurement] = None):
        self.path = path
        if measurements:
            self.measurements = measurements
        else:
            self.measurements = []
