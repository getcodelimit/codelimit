import os
from pathlib import Path
from typing import List, Annotated

import typer

from codelimit.common.CheckResult import CheckResult
from codelimit.common.Scanner import scan_codebase, is_excluded
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.tui.CodeLimitApp import CodeLimitApp
from codelimit.utils import upload_report, check_file

cli = typer.Typer(no_args_is_help=True, add_completion=False)


@cli.command(help="Check file(s)")
def check(
    paths: Annotated[List[Path], typer.Argument(exists=True)],
    quiet: Annotated[
        bool, typer.Option("--quiet", help="Not output when successful")
    ] = False,
):
    check_result = CheckResult()
    for path in paths:
        if path.is_file():
            check_file(path, check_result)
        elif path.is_dir():
            for root, dirs, files in os.walk(path.absolute()):
                files = [f for f in files if not f[0] == "."]
                dirs[:] = [d for d in dirs if not d[0] == "."]
                for file in files:
                    abs_path = Path(os.path.join(root, file))
                    rel_path = abs_path.relative_to(path.absolute())
                    if is_excluded(rel_path):
                        continue
                    check_file(abs_path, check_result)
    exit_code = 1 if check_result.unmaintainable > 0 else 0
    if (
        not quiet
        or check_result.hard_to_maintain > 0
        or check_result.unmaintainable > 0
    ):
        check_result.report()
    raise typer.Exit(code=exit_code)


@cli.command(help="Scan a codebase")
def scan(
    path: Annotated[
        Path, typer.Argument(exists=True, file_okay=False, help="Codebase root")
    ]
):
    cache_dir = path.joinpath(".codelimit_cache").resolve()
    report_path = cache_dir.joinpath("codelimit.json").resolve()
    if report_path.exists():
        cached_report = ReportReader.from_json(report_path.read_text())
    else:
        cached_report = None
    codebase = scan_codebase(path, cached_report)
    codebase.aggregate()
    report = Report(codebase)
    if not cache_dir.exists():
        cache_dir.mkdir()
        cache_dir_tag = cache_dir.joinpath("CACHEDIR.TAG").resolve()
        cache_dir_tag.write_text("Signature: 8a477f597d28d172789f06886806bc55")
        cache_dir_gitignore = cache_dir.joinpath(".gitignore").resolve()
        cache_dir_gitignore.write_text("# Created by codelimit automatically.\n*\n")
    report_path.write_text(ReportWriter(report).to_json())
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
