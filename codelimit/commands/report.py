from pathlib import Path

from rich.console import Console

from codelimit.common.report import format_markdown, format_text
from codelimit.common.report.ReportFormat import ReportFormat
from codelimit.utils import read_report


def report_command(path: Path, fmt: ReportFormat):
    stdout = Console(soft_wrap=True)
    report = read_report(path, stdout)
    if fmt == ReportFormat.markdown:
        format_markdown.print_report(report, stdout)
    else:
        format_text.print_report(report, stdout)
