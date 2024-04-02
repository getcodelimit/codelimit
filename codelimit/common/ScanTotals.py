from codelimit.common.LanguageTotals import LanguageTotals
from codelimit.common.SourceFileEntry import SourceFileEntry


class ScanTotals:
    def __init__(self) -> None:
        self._languages_totals: dict[str, LanguageTotals] = {}

    def add(self, entry: SourceFileEntry):
        if entry.language not in self._languages_totals:
            self._languages_totals[entry.language] = LanguageTotals(entry.language)
        self._languages_totals[entry.language].add(entry)

    def languages(self):
        return self._languages_totals.keys()

    def languages_totals(self) -> list[LanguageTotals]:
        return sorted(self._languages_totals.values(), key=lambda x: x.loc, reverse=True)

    def total_loc(self) -> int:
        return sum([l.loc for l in self._languages_totals.values()])

    def total_files(self) -> int:
        return sum([l.files for l in self._languages_totals.values()])

    def total_functions(self) -> int:
        return sum([l.functions for l in self._languages_totals.values()])

    def total_hard_to_maintain(self) -> int:
        return sum([l.hard_to_maintain for l in self._languages_totals.values()])

    def total_unmaintainable(self) -> int:
        return sum([l.unmaintainable for l in self._languages_totals.values()])