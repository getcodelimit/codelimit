from pathlib import Path

import requests  # type: ignore
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from codelimit.common.Measurement import Measurement
from codelimit.common.Scanner import languages, scan_file


def check_file(path: Path) -> list[Measurement]:
    result = []
    for language in languages:
        if language.accept_file(str(path.absolute())):
            measurements = scan_file(language, str(path))
            risks = sorted(
                [m for m in measurements if m.value > 30],
                key=lambda measurement: measurement.value,
                reverse=True,
            )
            result.extend(risks)
    return result


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
