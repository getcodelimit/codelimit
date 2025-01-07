from pathlib import Path

from rich.console import Console

from codelimit.common.report import format_markdown, format_text
from codelimit.common.report.ReportFormat import ReportFormat
from codelimit.utils import read_report, make_report_path


def report_command(path: Path, fmt: ReportFormat, diff_path: Path | None = None):
    stdout = Console(soft_wrap=True)
    report = read_report(make_report_path(path), stdout)
    diff_report = read_report(diff_path, stdout) if diff_path else None
    if fmt == ReportFormat.markdown:
        format_markdown.print_report(stdout, report, diff_report)
    else:
        format_text.print_report(stdout, report, diff_report)
