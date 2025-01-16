#!/usr/bin/env python3

# https://github.com/search?l=Go&o=desc&q=go&ref=advsearch&s=stars&type=Repositories
import os
import shutil
import tempfile
from pathlib import Path
from typing import Annotated

import typer
from sh import git

from codelimit.common.GithubRepository import GithubRepository
from codelimit.common.ScanResultTable import ScanResultTable
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.Scanner import scan_path
from codelimit.common.console import console
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.utils import info, success, fail


def load_report(path: Path) -> Report | None:
    report_file = path.joinpath('codelimit.json')
    if report_file.exists():
        return ReportReader.from_json(report_file.read_text())
    else:
        return None


def save_report(path: Path, report: Report) -> Path:
    report_json = ReportWriter(report).to_json()
    report_file = path.joinpath('codelimit.json')
    report_file.write_text(report_json)
    return report_file


def scan_repo(repo: GithubRepository) -> Report:
    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)
    info('Cloning repository...')
    git('clone', '--depth', '1', '--branch', repo.tag, f'https://github.com/{repo.owner}/{repo.name}.git')
    success('Repository cloned')
    info('Scanning codebase...')
    codebase = scan_path(Path(tmp_dir).joinpath(repo.name))
    success('Codebase scanned')
    shutil.rmtree(tmp_dir)
    codebase.aggregate()
    return Report(codebase)


def compare_reports(r1: Report, r2: Report) -> bool:
    if not len(r1.codebase.totals) == len(r2.codebase.totals):
        fail('Different number of languages')
        return False
    for lang in r1.codebase.totals:
        if not r1.codebase.totals[lang].is_equal(r2.codebase.totals[lang]):
            fail(f'Different totals for {lang}')
            return False
    return True


def run_repo(report_dir: Path) -> bool:
    result = True
    repo_parts = report_dir.name.split('_')
    repo = GithubRepository(repo_parts[0], repo_parts[1], tag=repo_parts[2])
    info(f'Scanning {repo}')
    new_report = scan_repo(repo)
    old_report = load_report(report_dir)
    if old_report:
        success('Existing report loaded')
        if compare_reports(old_report, new_report):
            success('No changes detected')
        else:
            print('Existing report:')
            console.print(ScanResultTable(ScanTotals(old_report.codebase.totals)), soft_wrap=True)
            print()
            print('New report:')
            console.print(ScanResultTable(ScanTotals(new_report.codebase.totals)), soft_wrap=True)
            fail('Changes detected')
            save_report(report_dir, new_report)
            success('New report saved')
            result = False
    else:
        save_report(report_dir, new_report)
        success('New report saved')
    return result


cli = typer.Typer(no_args_is_help=True, add_completion=False)


@cli.command(help="Run regression tests")
def run(example_dir: Annotated[
    Path, typer.Argument(exists=True, file_okay=False,
                         help="Example directory (e.g. examples/spring-projects_spring-boot_v3.4.0)")
] = None):
    exit_code = 0
    if example_dir:
        exit_code = 1 if not run_repo(example_dir.resolve()) else 0
    else:
        examples_dir = Path(os.path.abspath(__file__)).parent.parent.joinpath('examples')
        report_dirs = [d for d in examples_dir.iterdir() if d.is_dir()]
        for report_dir in report_dirs:
            if not run_repo(report_dir):
                exit_code = 1
    raise typer.Exit(code=exit_code)


@cli.command()
def add(repo: Annotated[str, typer.Argument(help="Repository (e.g. spring-projects/spring-boot)", show_default=False)],
        tag: Annotated[str, typer.Argument(show_default=False)]):
    """
    Add a repository.
    """
    [owner, name] = repo.split('/')
    report_dir = Path(os.path.abspath(__file__)).parent.parent.joinpath('examples').joinpath(f'{owner}_{name}_{tag}')
    if report_dir.exists():
        fail('Repository already exists')
    else:
        report_dir.mkdir()
        run_repo(report_dir)
        success('Example added')


if __name__ == '__main__':
    cli()
