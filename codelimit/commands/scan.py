from pathlib import Path
from typing import Optional

from rich.console import Console

from codelimit.common.Configuration import Configuration
from codelimit.common.Scanner import scan_codebase
from codelimit.common.report import format_text
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter


def scan_command(path: Path):
    stdout = Console(soft_wrap=True)
    cache_dir = path.joinpath(".codelimit_cache").resolve()
    report_path = cache_dir.joinpath("codelimit.json").resolve()
    cached_report = _read_cached_report(report_path)
    format_text.print_totals_header(stdout)
    codebase = scan_codebase(path, cached_report)
    codebase.aggregate()
    report = Report(codebase, Configuration.repository)
    format_text.print_summary(report, stdout)
    if not cache_dir.exists():
        cache_dir.mkdir()
        cache_dir_tag = cache_dir.joinpath("CACHEDIR.TAG").resolve()
        cache_dir_tag.write_text("Signature: 8a477f597d28d172789f06886806bc55")
        cache_dir_gitignore = cache_dir.joinpath(".gitignore").resolve()
        cache_dir_gitignore.write_text("# Created by codelimit automatically.\n*\n")
    report_path.write_text(ReportWriter(report).to_json())


def _read_cached_report(report_path: Path) -> Optional[Report]:
    if report_path.exists():
        cached_report = ReportReader.from_json(report_path.read_text())
        if cached_report and cached_report.version == Report.VERSION:
            return cached_report
    return None
