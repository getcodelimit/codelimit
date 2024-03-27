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
