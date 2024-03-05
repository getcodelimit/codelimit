from pathlib import Path
from typing import Optional

import requests  # type: ignore
import typer
from pygments.lexers import get_lexer_for_filename
from rich.progress import Progress, SpinnerColumn, TextColumn

from codelimit.common.CheckResult import CheckResult
from codelimit.common.Scanner import scan_file
from codelimit.languages import languages
from codelimit.common.lexer_utils import lex
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.common.utils import load_scope_extractor_by_name


def check_file(path: Path, check_result: CheckResult):
    lexer = get_lexer_for_filename(path)
    language = lexer.__class__.name
    if language in languages:
        with open(path) as f:
            code = f.read()
        tokens = lex(lexer, code, False)
        scope_extractor = load_scope_extractor_by_name(lexer.__class__.name)
        if scope_extractor:
            measurements = scan_file(tokens, scope_extractor)
            risks = sorted(
                [m for m in measurements if m.value > 30],
                key=lambda measurement: measurement.value,
                reverse=True,
            )
            check_result.add(path, risks)


def read_cached_report(path: Path) -> Optional[Report]:
    cache_dir = path.joinpath(".codelimit_cache").resolve()
    report_path = cache_dir.joinpath("codelimit.json").resolve()
    if report_path.exists():
        return ReportReader.from_json(report_path.read_text())
    else:
        return None


def upload_report(
    report: Report, repository: str, branch: str, url: str, token: str
) -> None:
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
