#!/usr/bin/env python3

# https://github.com/search?l=Go&o=desc&q=go&ref=advsearch&s=stars&type=Repositories
import os
import shutil
import tempfile
from pathlib import Path

from halo import Halo
from rich.console import Console
from sh import git

from codelimit.common.ScanResultTable import ScanResultTable
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.Scanner import scan_folder
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter

examples_dir = Path(os.path.abspath(__file__)).parent.parent.joinpath('examples')
console = Console()


def info(text: str):
    console.print(f'[bold]ℹ︎[/bold] {text}', soft_wrap=True)


def success(text: str):
    console.print(f'[green]✔[/green] {text}', soft_wrap=True)


def fail(text: str):
    console.print(f'[red]⨯[/red] {text}', soft_wrap=True)


def load_report(owner: str, name: str, tag: str) -> Report | None:
    report_dir = examples_dir.joinpath(f'{owner}_{name}_{tag}')
    report_file = report_dir.joinpath('codelimit.json')
    if report_file.exists():
        return ReportReader.from_json(report_file.read_text())
    else:
        return None


def save_report(owner: str, name: str, tag: str, report: Report) -> Path:
    report_json = ReportWriter(report).to_json()
    report_dir = examples_dir.joinpath(f'{owner}_{name}_{tag}')
    os.makedirs(report_dir, exist_ok=True)
    report_file = report_dir.joinpath('codelimit.json')
    report_file.write_text(report_json)
    return report_file


def scan_repo(owner: str, name: str, tag: str) -> Report:
    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)
    spinner = Halo(text='Cloning repository', spinner='dots')
    spinner.start()
    git('clone', '--depth', '1', '--branch', tag, f'https://github.com/{owner}/{name}.git')
    spinner.succeed('Repository cloned')
    spinner = Halo(text='Scanning codebase', spinner='dots')
    spinner.start()
    codebase = scan_folder(Path(tmp_dir).joinpath(name))
    spinner.succeed('Codebase scanned')
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


if __name__ == '__main__':
    exit_code = 0
    repos = [
        ('getcodelimit', 'battlesnake-challenge', '20241209'),
        ('spring-projects', 'spring-boot', 'v3.4.0'),
    ]
    for repo in repos:
        info(f'Scanning {repo[0]}/{repo[1]}@{repo[2]}')
        old_report = load_report(repo[0], repo[1], repo[2])
        if old_report:
            success('Existing report loaded')
        new_report = scan_repo(repo[0], repo[1], repo[2])
        if old_report:
            if compare_reports(old_report, new_report):
                success('No changes detected')
            else:
                print('Existing report:')
                console.print(ScanResultTable(ScanTotals(old_report.codebase.totals)), soft_wrap=True)
                print()
                print('Current report:')
                console.print(ScanResultTable(ScanTotals(new_report.codebase.totals)), soft_wrap=True)
                fail('Changes detected')
                exit_code = 1
        else:
            new_report_file = save_report(repo[0], repo[1], repo[2], new_report)
            success(f'Report written to {new_report_file}')
    exit(exit_code)
