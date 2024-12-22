from pathlib import Path

from rich.console import Console

from codelimit.commands.report import ReportFormat
from codelimit.common.report import format_markdown, format_text
from codelimit.utils import read_report


def findings_command(path: Path, fmt: ReportFormat):
    stdout = Console(soft_wrap=True)
    report = read_report(path)
    if fmt == ReportFormat.markdown:
        format_markdown.print_findings(report, stdout, True)
    else:
        format_text.print_findings(report, stdout, True)