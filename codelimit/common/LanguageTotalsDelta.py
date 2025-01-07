from codelimit.common.LanguageTotals import LanguageTotals


class LanguageTotalsDelta:
    def __init__(self, language_totals_current: LanguageTotals, language_totals_previous: LanguageTotals | None):
        self._language_totals_current = language_totals_current
        self._language_totals_previous = language_totals_previous

    def files(self) -> str:
        total_files = self._language_totals_current.files
        delta = total_files - (self._language_totals_previous.files if self._language_totals_previous else 0)
        return f"{total_files:n}" if delta == 0 else f"{total_files:n} ({delta:+n})"

    def functions(self) -> str:
        total_functions = self._language_totals_current.functions
        delta = total_functions - (self._language_totals_previous.functions if self._language_totals_previous else 0)
        return f"{total_functions:n}" if delta == 0 else f"{total_functions:n} ({delta:+n})"

    def loc(self) -> str:
        total_loc = self._language_totals_current.loc
        delta = total_loc - (self._language_totals_previous.loc if self._language_totals_previous else 0)
        return f"{total_loc:n}" if delta == 0 else f"{total_loc:n} ({delta:+n})"

    def hard_to_maintain(self) -> str:
        total_hard_to_maintain = self._language_totals_current.hard_to_maintain
        if self._language_totals_previous:
            delta = total_hard_to_maintain - self._language_totals_previous.hard_to_maintain
            return f"{total_hard_to_maintain:n}" if delta == 0 else f"{total_hard_to_maintain:n} ({delta:+n})"
        else:
            return f"{total_hard_to_maintain:n}"

    def unmaintainable(self) -> str:
        total_unmaintainable = self._language_totals_current.unmaintainable
        if self._language_totals_previous:
            delta = total_unmaintainable - self._language_totals_previous.unmaintainable
            return f"{total_unmaintainable:n}" if delta == 0 else f"{total_unmaintainable:n} ({delta:+n})"
        else:
            return f"{total_unmaintainable:n}"
