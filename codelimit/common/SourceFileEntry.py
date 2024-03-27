from codelimit.common.CodebseEntry import CodebaseEntry
from codelimit.common.Measurement import Measurement
from codelimit.common.utils import make_profile


class SourceFileEntry(CodebaseEntry):
    def __init__(
        self,
        path: str,
        checksum: str,
        language: str,
        loc: int,
        measurements: list[Measurement],
    ):
        super().__init__(path)
        profile = make_profile(measurements)
        self._checksum = checksum
        self.language = language
        self.loc = loc
        self._profile: list[int] = profile
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
