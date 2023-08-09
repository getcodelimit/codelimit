from pathlib import Path
from typing import List

import typer

from codelimit.common.Scanner import scan, scan_file
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportUnit import ReportUnit, format_report_unit
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.languages.python.PythonLaguage import PythonLanguage
from codelimit.tui.CodeLimitApp import CodeLimitApp
from codelimit.utils import upload_report
from rich import print

cli = typer.Typer()
pre_commit_hook = typer.Typer()


@cli.callback(invoke_without_command=True)
def cli_callback(
    path: Path,
    report_path: Path = typer.Option(
        None,
        "--report",
        "-r",
        help="JSON report for a code base",
    ),
    upload: bool = typer.Option(False, "--upload", help="Upload a report"),
    url: str = typer.Option(
        "https://codelimit-web.vercel.app/api/upload",
        "--url",
        "-u",
        help="Upload JSON report to this URL.",
    ),
) -> None:
    """CodeLimit: Your refactoring alarm"""

    report_path = report_path or path.joinpath("codelimit.json").resolve()

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


@pre_commit_hook.callback(invoke_without_command=True)
def pre_commit_hook_callback(paths: List[Path]):
    exit_code = 0
    language = PythonLanguage()
    for path in paths:
        measurements = scan_file(language, str(path))
        medium_risk = sorted(
            [m for m in measurements if 30 < m.value <= 60],
            key=lambda measurement: measurement.value,
            reverse=True,
        )
        high_risk = sorted(
            [m for m in measurements if m.value > 60],
            key=lambda measurement: measurement.value,
            reverse=True,
        )
        if medium_risk:
            print(f"🔔 {path}")
            for m in medium_risk:
                print(format_report_unit(ReportUnit(str(path), m)))
        if high_risk:
            print(f"🚨 {path}")
            for m in high_risk:
                print(format_report_unit(ReportUnit(str(path), m)))
            exit_code = 1
    raise typer.Exit(code=exit_code)


if __name__ == "__main__":
    cli()
