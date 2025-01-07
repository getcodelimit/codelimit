from codelimit.common.ScanTotals import ScanTotals


class ScanTotalsDelta:
    def __init__(self, scan_totals_current: ScanTotals, scan_totals_previous: ScanTotals):
        self._scan_totals_current = scan_totals_current
        self._scan_totals_previous = scan_totals_previous

    def total_files(self) -> str:
        total_files = self._scan_totals_current.total_files()
        delta = total_files - self._scan_totals_previous.total_files()
        return f"{total_files:n}" if delta == 0 else f"{total_files:n} ({delta:+n})"

    def total_functions(self) -> str:
        total_functions = self._scan_totals_current.total_functions()
        delta = total_functions - self._scan_totals_previous.total_functions()
        return f"{total_functions:n}" if delta == 0 else f"{total_functions:n} ({delta:+n})"

    def total_loc(self) -> str:
        total_loc = self._scan_totals_current.total_loc()
        delta = total_loc - self._scan_totals_previous.total_loc()
        return f"{total_loc:n}" if delta == 0 else f"{total_loc:n} ({delta:+n})"

    def total_hard_to_maintain(self) -> str:
        hard_to_maintain = self._scan_totals_current.total_hard_to_maintain()
        delta = hard_to_maintain - self._scan_totals_previous.total_hard_to_maintain()
        return f"{hard_to_maintain:n}" if delta == 0 else f"{hard_to_maintain:n} ({delta:+n})"

    def total_unmaintainable(self) -> str:
        unmaintainable = self._scan_totals_current.total_unmaintainable()
        delta = unmaintainable - self._scan_totals_previous.total_unmaintainable()
        return f"{unmaintainable:n}" if delta == 0 else f"{unmaintainable:n} ({delta:+n})"
