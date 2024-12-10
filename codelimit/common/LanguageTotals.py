from __future__ import annotations

from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.utils import make_count_profile


class LanguageTotals:
    def __init__(self, language: str):
        self.language = language
        self.files = 0
        self.loc = 0
        self.functions = 0
        self.hard_to_maintain = 0
        self.unmaintainable = 0

    def add(self, entry: SourceFileEntry):
        profile = make_count_profile(entry.measurements())
        self.files += 1
        self.loc += entry.loc
        self.functions += len(entry.measurements())
        self.hard_to_maintain += profile[2]
        self.unmaintainable += profile[3]

    def is_equal(self, other: LanguageTotals) -> bool:
        return (
                self.language == other.language and
                self.files == other.files and
                self.loc == other.loc and
                self.functions == other.functions and
                self.hard_to_maintain == other.hard_to_maintain and
                self.unmaintainable == other.unmaintainable
        )
