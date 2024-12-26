from pathlib import Path
from typing import List, Annotated, Optional

import pyperclip
import typer
from click import Context
from rich import print
from typer.core import TyperGroup

from codelimit.commands.check import check_command
from codelimit.commands.findings import findings_command
from codelimit.commands.report import ReportFormat, report_command
from codelimit.commands.scan import scan_command
from codelimit.common.Configuration import Configuration, setup_logging
from codelimit.common.utils import configure_github_repository
from codelimit.utils import success, fail
from codelimit.version import version


class OrderCommands(TyperGroup):
    def list_commands(self, ctx: Context):
        return list(self.commands)


cli = typer.Typer(cls=OrderCommands, no_args_is_help=True, add_completion=False)


# cli.add_typer(app.app, name="app", help="Code Limit GitHub App commands")


@cli.command(help="Scan a codebase")
def scan(
        path: Annotated[
            Path, typer.Argument(exists=True, file_okay=False, help="Codebase root")
        ] = Path("."),
        exclude: Annotated[
            Optional[list[str]], typer.Option(help="Glob patterns for exclusion")
        ] = None,
        verbose: Annotated[
            Optional[bool], typer.Option("--verbose", "-v", help="Verbose output")
        ] = False,
):
    if exclude:
        Configuration.exclude.extend(exclude)
    if verbose:
        Configuration.verbose = True
    Configuration.load(path)
    setup_logging()
    configure_github_repository(path)
    scan_command(path)


@cli.command(help="Show report for codebase")
def report(
        path: Annotated[
            Path, typer.Argument(exists=True, file_okay=False, help="Codebase root")
        ] = Path("."),
        fmt: Annotated[
            ReportFormat, typer.Option("--format", help="Output format")
        ] = ReportFormat.text,
):
    Configuration.load(path)
    report_command(path, fmt)


@cli.command(help="Show findings for codebase")
def findings(
        path: Annotated[
            Path, typer.Argument(exists=True, file_okay=False, help="Codebase root")
        ] = Path("."),
        full: Annotated[bool, typer.Option("--full", help="Show full findings")] = False,
        fmt: Annotated[
            ReportFormat, typer.Option("--format", help="Output format")
        ] = ReportFormat.text,
):
    Configuration.load(path)
    findings_command(path, full, fmt)


@cli.command(help="Check file(s)")
def check(
        paths: Annotated[List[Path], typer.Argument(exists=True)],
        exclude: Annotated[
            Optional[list[str]], typer.Option(help="Glob patterns for exclusion")
        ] = None,
        quiet: Annotated[
            bool, typer.Option("--quiet", help="No output when successful")
        ] = False,
        verbose: Annotated[
            Optional[bool], typer.Option("--verbose", "-v", help="Verbose output")
        ] = False,
):
    if exclude:
        Configuration.exclude.extend(exclude)
    if verbose:
        Configuration.verbose = True
    Configuration.load(Path('.'))
    setup_logging()
    check_command(paths, quiet)


@cli.command(help="Generate badge Markdown")
def badge(
        path: Annotated[
            Path, typer.Argument(exists=True, file_okay=False, help="Codebase root")
        ] = Path(".")
):
    Configuration.load(path)
    configure_github_repository(path)
    if not Configuration.repository:
        fail("Could not determine repository information.")
        raise typer.Exit(1)
    owner = Configuration.repository.owner
    name = Configuration.repository.name
    branch = Configuration.repository.branch
    badge_markdown = (f'[![CodeLimit](https://github.com/{owner}/{name}/blob/_codelimit_reports/{branch}/badge.svg)]('
                      f'https://github.com/{owner}/{name}/blob/_codelimit_reports/{branch}/codelimit.md)')
    print(f'{badge_markdown}\n')
    pyperclip.copy(badge_markdown)
    success("Badge Markdown copied to clipboard!")


def _version_callback(show: bool):
    if show:
        print(f"Code Limit version: {version}")
        raise typer.Exit()


@cli.callback()
def main(
        version: Annotated[
            Optional[bool],
            typer.Option(
                "--version", "-V", help="Show version", callback=_version_callback
            ),
        ] = None,
):
    """Code Limit: Your refactoring alarm."""

    if version:
        raise typer.Exit()


if __name__ == "__main__":
    cli()
