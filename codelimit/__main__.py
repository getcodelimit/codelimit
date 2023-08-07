""" CodeLimit Command-Line Interface
"""

from pathlib import Path

import requests
import typer

from rich.progress import Progress, SpinnerColumn, TextColumn

from .common.Scanner import scan
from .common.report.Report import Report
from .common.report.ReportReader import ReportReader
from .common.report.ReportWriter import ReportWriter
from .tui.CodeLimitApp import CodeLimitApp


cli = typer.Typer()

_CODELIMIT_UPLOAD_URL: str = "https://codelimit-web.vercel.app/api/upload"


@cli.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    path: Path,
    report_path: Path = typer.Option(
        None,
        "--report",
        "-r",
        help="JSON report for a code base",
    ),
    upload: bool = typer.Option(False, "--upload", help="Upload a report"),
    url: str = typer.Option(
        _CODELIMIT_UPLOAD_URL,
        "--url",
        "-u",
        help="Upload JSON report to this URL.",
    ),
) -> None:
    """CodeLimit code refactorization visualizer

    More stuff goes here.
    """

    report_path = report_path or Path(f"{path.name}-codelimit.json").resolve()

    if upload:
        try:
            upload_report(report_path, url)
            raise typer.Exit(code=0)
        except FileNotFoundError as error:
            typer.secho(f"File not found: {error}", fg="red")
        raise typer.Exit(code=1) from None

    if not report_path.exists():
        codebase = scan(path)
        codebase.aggregate()
        report = Report(codebase)
        report_path.write_text(ReportWriter(report).to_json())
    else:
        report = ReportReader.from_json(report_path.read_text())

    app = CodeLimitApp(report)
    app.run()


def upload_report(path: Path, url: str) -> None:
    """Upload a CodeLimit JSON Report"""

    data_template = (
        '{{"repository": "getcodelimit/codelimit", "branch": "main", "report":{}}}'
    )

    if not path.exist():
        raise FileNotFoundError(str(path))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Uploading {path.name} to {url}", total=None)
        result = requests.post(
            url,
            data=data_template.format(path.read_text()),
            headers={"Content-Type": "application/json"},
        )

    if result.ok:
        typer.secho("Uploaded", fg="green")
    else:
        typer.secho(f"Upload unsuccessful: {result.status_code}", fg="red")
        raise typer.Exit(exit_code=1)


if __name__ == "__main__":
    cli()
