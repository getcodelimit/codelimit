from codelimit.common.LanguageTotals import LanguageTotals
from codelimit.common.SourceFileEntry import SourceFileEntry


class ScanTotals:
    def __init__(
        self, language_totals: dict[str, LanguageTotals] | None = None
    ) -> None:
        self._languages_totals: dict[str, LanguageTotals] = (
            language_totals if language_totals else {}
        )

    def add(self, entry: SourceFileEntry):
        if entry.language not in self._languages_totals:
            self._languages_totals[entry.language] = LanguageTotals(entry.language)
        self._languages_totals[entry.language].add(entry)

    def languages(self):
        return self._languages_totals.keys()

    def languages_totals(self) -> list[LanguageTotals]:
        return sorted(
            self._languages_totals.values(), key=lambda x: x.loc, reverse=True
        )

    def total_loc(self) -> int:
        return sum([language.loc for language in self._languages_totals.values()])

    def total_files(self) -> int:
        return sum([language.files for language in self._languages_totals.values()])

    def total_functions(self) -> int:
        return sum([language.functions for language in self._languages_totals.values()])

    def total_hard_to_maintain(self) -> int:
        return sum(
            [language.hard_to_maintain for language in self._languages_totals.values()]
        )

    def total_unmaintainable(self) -> int:
        return sum(
            [language.unmaintainable for language in self._languages_totals.values()]
        )
