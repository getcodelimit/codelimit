from pathlib import Path
from typing import List, Annotated

import typer

from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.tui.CodeLimitApp import CodeLimitApp
from codelimit.utils import upload_report, generate_report, check_files

cli = typer.Typer(no_args_is_help=True, add_completion=False)


@cli.command(help="Scan a codebase")
def scan(
    path: Annotated[
        Path, typer.Argument(file_okay=False, exists=True, help="Codebase root")
    ]
):
    report_path = path.joinpath("codelimit.json").resolve()
    if not report_path.exists():
        report = generate_report(path)
        report_path.write_text(ReportWriter(report).to_json())
    else:
        report = ReportReader.from_json(report_path.read_text())
    app = CodeLimitApp(report)
    app.run()


@cli.command(help="Check file(s)")
def check(paths: List[Path]):
    exit_code = check_files(paths)
    raise typer.Exit(code=exit_code)


@cli.command(help="Upload report to CodeLimit server", hidden=True)
def upload(
    report_path: Path = typer.Argument(help="JSON report for a code base"),
    url: str = typer.Option(
        "https://codelimit-web.vercel.app/api/upload",
        "--url",
        "-u",
        help="Upload JSON report to this URL.",
    ),
):
    try:
        upload_report(report_path, url)
        raise typer.Exit(code=0)
    except FileNotFoundError as error:
        typer.secho(f"File not found: {error}", fg="red")
    raise typer.Exit(code=1) from None


@cli.callback()
def main():
    """CodeLimit: Your refactoring alarm"""


if __name__ == "__main__":
    cli()
