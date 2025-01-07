from pathlib import Path

from rich.console import Console

from codelimit.commands.report import ReportFormat
from codelimit.common.report import format_markdown, format_text
from codelimit.utils import read_report, make_report_path


def findings_command(path: Path, full: bool, fmt: ReportFormat):
    stdout = Console(soft_wrap=True)
    report = read_report(make_report_path(path), stdout)
    if fmt == ReportFormat.markdown:
        format_markdown.print_findings(report, stdout, full)
    else:
        format_text.print_findings(stdout, report, full)
