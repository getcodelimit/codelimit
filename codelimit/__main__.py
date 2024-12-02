from pathlib import Path
from typing import List, Annotated, Optional

import typer
from click import Context
from rich import print
from typer.core import TyperGroup

from codelimit.commands import app
from codelimit.commands.check import check_command
from codelimit.commands.report import report_command, ReportFormat
from codelimit.commands.scan import scan_command
from codelimit.common.Configuration import Configuration
from codelimit.version import version


class OrderCommands(TyperGroup):
    def list_commands(self, ctx: Context):
        return list(self.commands)


cli = typer.Typer(cls=OrderCommands, no_args_is_help=True, add_completion=False)
cli.add_typer(app.app, name="app", help="Code Limit GitHub App commands")


@cli.command(help="Check file(s)")
def check(
    paths: Annotated[List[Path], typer.Argument(exists=True)],
    quiet: Annotated[
        bool, typer.Option("--quiet", help="No output when successful")
    ] = False,
):
    check_command(paths, quiet)


@cli.command(help="Scan a codebase")
def scan(
    path: Annotated[
        Path, typer.Argument(exists=True, file_okay=False, help="Codebase root")
    ] = Path(".")
):
    scan_command(path)


@cli.command(help="Show report for codebase")
def report(
    path: Annotated[
        Path, typer.Argument(exists=True, file_okay=False, help="Codebase root")
    ] = Path("."),
    full: Annotated[bool, typer.Option("--full", help="Show full report")] = False,
    totals: Annotated[bool, typer.Option("--totals", help="Only show totals")] = False,
    fmt: Annotated[
        ReportFormat, typer.Option("--format", help="Output format")
    ] = ReportFormat.text,
):
    report_command(path, full, totals, fmt)


def _version_callback(show: bool):
    if show:
        print(f"Code Limit version: {version}")
        raise typer.Exit()


@cli.callback()
def main(
    verbose: Annotated[
        Optional[bool], typer.Option("--verbose", "-v", help="Verbose output")
    ] = False,
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
    if verbose:
        Configuration.verbose = True
    if version:
        raise typer.Exit()
    if exclude:
        Configuration.excludes.extend(exclude)


if __name__ == "__main__":
    cli()
