from pathlib import Path
from typing import Optional

import requests  # type: ignore
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from codelimit.common.console import console
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter


def info(text: str):
    console.print(f'[bold]ℹ︎[/bold] {text}', soft_wrap=True)


def success(text: str):
    console.print(f'[green]✔[/green] {text}', soft_wrap=True)


def fail(text: str):
    console.print(f'[red]⨯[/red] {text}', soft_wrap=True)


def make_report_path(root: Path) -> Path:
    return root.joinpath(".codelimit_cache").resolve().joinpath("codelimit.json")


def read_cached_report(path: Path) -> Optional[Report]:
    cache_dir = path.joinpath(".codelimit_cache").resolve()
    report_path = cache_dir.joinpath("codelimit.json").resolve()
    if report_path.exists():
        return ReportReader.from_json(report_path.read_text())
    else:
        return None


def read_report(report_path: Path, console: Console) -> Report:
    if not report_path.exists():
        console.print("[red]No cached report found, run scan first[/red]")
        raise typer.Exit(code=1)
    report_data = report_path.read_text()
    report_version = ReportReader.get_report_version(report_data)
    if report_version != Report.VERSION:
        console.print("[red]Report version mismatch, run scan first[/red]")
        raise typer.Exit(code=1)
    return ReportReader.from_json(report_data)


def upload_report(
        report: Report, repository: str, branch: str, url: str, token: str
) -> None:
    result = api_post_report(report, branch, repository, url, token)
    if result.ok:
        typer.secho("Upload successful!", fg="green")
    else:
        error_message = "Upload unsuccessful: "
        if result.text:
            error_message += result.text
        else:
            error_message += str(result.status_code)
        typer.secho(error_message, fg="red")
        raise typer.Exit(code=1)


def api_post_report(report, branch, repository, url, token):
    data_template = (
        f'{{{{"repository": "{repository}", "branch": "{branch}", "report":{{}}}}}}'
    )
    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
    ) as progress:
        progress.add_task(description=f"Uploading report to {url}", total=None)
        result = requests.post(
            url,
            data=data_template.format(
                ReportWriter(report, pretty_print=False).to_json()
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
    return result
