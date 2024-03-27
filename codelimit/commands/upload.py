from pathlib import Path

import typer

from codelimit.common.report.ReportReader import ReportReader
from codelimit.github_auth import get_github_token
from codelimit.utils import read_cached_report, upload_report


def upload_command(
    repository: str, branch: str, report_file: Path, token: str, url: str
):
    if report_file:
        report = ReportReader.from_json(report_file.read_text())
        if not report:
            print("[red]Could not read report file[/red]")
            raise typer.Exit(code=1)
    else:
        cached_report = read_cached_report(Path("."))
        if not cached_report:
            print("[red]No cached report found in current folder[/red]")
            raise typer.Exit(code=1)
        else:
            report = cached_report
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
