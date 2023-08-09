from abc import ABC, abstractmethod

from codelimit.common.utils import get_basename


class CodebaseEntry(ABC):
    def __init__(self, path: str):
        self.path = path
        self.name = get_basename(path)
        if self.is_folder():
            self.name += "/"

    @abstractmethod
    def is_folder(self):
        pass

    @abstractmethod
    def is_file(self):
        pass

    @property
    def profile(self):
        return None

    @property
    def checksum(self):
        return None
