from pathlib import Path
from typing import List

import requests  # type: ignore
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from codelimit.common.Scanner import scan, scan_file
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportUnit import format_report_unit, ReportUnit
from codelimit.languages.python.PythonLaguage import PythonLanguage


def generate_report(path: Path) -> Report:
    codebase = scan(path)
    codebase.aggregate()
    return Report(codebase)


def check_files(paths: List[Path]):
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
        if high_risk:
            print(f"🚨 {path}")
            for m in high_risk:
                print(format_report_unit(ReportUnit(str(path), m)))
            exit_code = 1
        if medium_risk:
            print(f"🔔 {path}")
            for m in medium_risk:
                print(format_report_unit(ReportUnit(str(path), m)))
    return exit_code


def upload_report(path: Path, url: str) -> None:
    data_template = (
        '{{"repository": "getcodelimit/codelimit", "branch": "main", "report":{}}}'
    )

    if not path.exists():
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
