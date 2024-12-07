from pathlib import Path

import typer

from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.github_auth import get_github_token
from codelimit.utils import upload_report, make_report_path


def upload_command(
    repository: str, branch: str, report_file: Path, token: str, url: str
):
    if report_file:
        report = ReportReader.from_json(report_file.read_text())
        if not report:
            print("[red]Could not read report file[/red]")
            raise typer.Exit(code=1)
    else:
        report_path = make_report_path(Path("."))
        if not report_path.exists():
            print("[red]No cached report found, run scan first[/red]")
            raise typer.Exit(code=1)
        report_data = report_path.read_text()
        report_version = ReportReader.get_report_version(report_data)
        if report_version != Report.VERSION:
            print("[red]Report version mismatch, run scan first[/red]")
            raise typer.Exit(code=1)
        report = ReportReader.from_json(report_data)
    if not token:
        token = get_github_token()
        if not token:
            print("[red]Invalid or no credentials, please login or supply token[/red]")
            raise typer.Exit(code=1)
    try:
        upload_report(report, repository, branch, url, token)
        raise typer.Exit(code=0)
    except FileNotFoundError as error:
        typer.secho(f"File not found: {error}", fg="red")
    raise typer.Exit(code=1) from None
