from typing import Union

from codelimit.common.SourceFile import SourceFile
from codelimit.common.utils import risk_categories


class SourceFolderEntry:
    def __init__(self, name: str):
        self.name = name
        self.loc: Union[int, None] = None
        self.risk_categories: Union[list[int], None] = None

    def update(self, file: SourceFile):
        file_loc = sum([m.value for m in file.measurements])
        if self.loc:
            self.loc += file_loc
        else:
            self.loc = file_loc
        file_rc = risk_categories(file.measurements)
        if self.risk_categories:
            self.risk_categories[0] += file_rc[0]
            self.risk_categories[1] += file_rc[1]
            self.risk_categories[2] += file_rc[2]
            self.risk_categories[3] += file_rc[3]
        else:
            self.risk_categories = file_rc
