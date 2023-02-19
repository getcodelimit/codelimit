from codelimit.common.CodebseEntry import CodebaseEntry
from codelimit.common.Measurement import Measurement
from codelimit.common.utils import make_profile


class SourceFileEntry(CodebaseEntry):
    def __init__(self, path: str, checksum: str, measurements: list[Measurement]):
        super().__init__(path)
        profile = make_profile(measurements)
        self._profile: list[int] = profile
        self._checksum = checksum
        self._measurements = measurements

    def is_folder(self):
        return False

    def is_file(self):
        return True

    def profile(self):
        return self._profile

    def checksum(self):
        return self._checksum

    def measurements(self):
        return self._measurements
