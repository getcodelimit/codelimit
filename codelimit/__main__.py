import os
from pathlib import Path
from typing import List, Annotated

import typer

from codelimit.common.CheckResult import CheckResult
from codelimit.common.Scanner import scan_codebase
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.tui.CodeLimitApp import CodeLimitApp
from codelimit.utils import upload_report, check_file

cli = typer.Typer(no_args_is_help=True, add_completion=False)


@cli.command(help="Check file(s)")
def check(
    paths: Annotated[List[Path], typer.Argument(exists=True, help="Codebase root")],
    quiet: Annotated[
        bool, typer.Option("--quiet", help="Not output when successful")
    ] = False,
):
    check_result = CheckResult()
    for path in paths:
        if path.is_file():
            check_result.add(path, check_file(path))
        elif path.is_dir():
            for root, dirs, files in os.walk(path.absolute()):
                files = [f for f in files if not f[0] == "."]
                dirs[:] = [d for d in dirs if not d[0] == "."]
                for file in files:
                    file_path = Path(os.path.join(root, file))
                    check_result.add(file_path, check_file(file_path))
    exit_code = 1 if check_result.unmaintainable > 0 else 0
    if (
        not quiet
        or check_result.hard_to_maintain > 0
        or check_result.unmaintainable > 0
    ):
        check_result.report()
    raise typer.Exit(code=exit_code)


@cli.command(help="Scan a codebase")
def scan(path: Annotated[Path, typer.Argument()] = Path(".")):
    report_path = path.joinpath("codelimit.json").resolve()
    if not report_path.exists():
        codebase = scan_codebase(path)
        codebase.aggregate()
        report = Report(codebase)
        report_path.write_text(ReportWriter(report).to_json())
    else:
        report = ReportReader.from_json(report_path.read_text())
    app = CodeLimitApp(report)
    app.run()


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
    """CodeLimit: Your refactoring alarm."""


if __name__ == "__main__":
    cli()
