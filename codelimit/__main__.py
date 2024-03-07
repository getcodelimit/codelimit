import importlib.metadata
import os
from pathlib import Path
from typing import List, Annotated, Optional

import typer
from rich import print

from codelimit.commands import github
from codelimit.common.CheckResult import CheckResult
from codelimit.common.Configuration import Configuration
from codelimit.common.Scanner import scan_codebase, is_excluded
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.github_auth import get_github_token
from codelimit.utils import upload_report, check_file, read_cached_report

cli = typer.Typer(no_args_is_help=True, add_completion=False)
cli.add_typer(github.app, name="github", help="GitHub commands")


@cli.command(help="Check file(s)")
def check(
    paths: Annotated[List[Path], typer.Argument(exists=True)],
    quiet: Annotated[
        bool, typer.Option("--quiet", help="No output when successful")
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
    cached_report = _read_cached_report(report_path)
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
    # if sys.stdout.isatty():
    #     app = CodeLimitApp(report)
    #     app.run()


def _read_cached_report(report_path: Path) -> Optional[Report]:
    if report_path.exists():
        cached_report = ReportReader.from_json(report_path.read_text())
        if cached_report and cached_report.version == Report.VERSION:
            return cached_report
    return None


@cli.command(help="Upload report to Code Limit")
def upload(
    repository: Annotated[
        str,
        typer.Argument(
            envvar="GITHUB_REPOSITORY", show_default=False, help="GitHub repository"
        ),
    ],
    branch: Annotated[
        str,
        typer.Argument(envvar="GITHUB_REF", show_default=False, help="GitHub branch"),
    ],
    report_file: Path = typer.Option(
        None,
        "--report",
        exists=True,
        dir_okay=False,
        file_okay=True,
        help="JSON report file",
    ),
    token: str = typer.Option(None, "--token", help="GitHub access token"),
    url: str = typer.Option(
        "https://codelimit.vercel.app/api/upload",
        "--url",
        help="Upload JSON report to this URL.",
    ),
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


def _version_callback(show: bool):
    if show:
        version = importlib.metadata.version("codelimit")
        print(f"Code Limit version: {version}")
        raise typer.Exit()


@cli.callback()
def main(
    exclude: Annotated[
        Optional[list[str]], typer.Option(help="Glob patterns for exclusion")
    ] = None,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", "-V", help="Show version", callback=_version_callback
        ),
    ] = None,
):
    """CodeLimit: Your refactoring alarm."""
    if exclude:
        Configuration.excludes.extend(exclude)


if __name__ == "__main__":
    cli()
