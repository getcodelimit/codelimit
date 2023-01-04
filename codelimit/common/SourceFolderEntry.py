from typing import Union

from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.utils import make_profile


class SourceFolderEntry:
    def __init__(self, name: str, measurements: list[SourceMeasurement] = None):
        self.name = name
        profile = make_profile(measurements) if measurements else None
        self.profile: Union[list[int], None] = profile

    def is_folder(self):
        return self.name.endswith('/')

    def is_file(self):
        return not self.is_folder()
