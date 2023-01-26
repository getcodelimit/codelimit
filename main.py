#!/usr/bin/env python3
import os.path
from pathlib import Path

import click

from codelimit.common.Scanner import Scanner
from codelimit.common.report.RefactorList import RefactorList
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.common.utils import get_parent_folder


@click.command()
@click.argument('path', type=click.Path(exists=True, file_okay=True, dir_okay=True, path_type=Path))
@click.option('--scan', is_flag=True)
def cli(path: Path, scan: bool):
    if os.path.isdir(path):
        if os.path.exists(os.path.join(path, 'codelimit.json')):
            if scan:
                scan_path(path)
            tui(Path(os.path.join(path, 'codelimit.json')))
        else:
            scan_path(path)
    else:
        if os.path.basename(path) == 'codelimit.json':
            tui(path)
        else:
            print('usage')
    pass


def scan_path(path: Path):
    codebase = Scanner().scan(path)
    codebase.aggregate()
    print(f'Total lines of code: {codebase.total_loc()}')
    report = Report(codebase)

    report_file = os.path.join(path, 'codelimit.json')
    with open(report_file, 'w') as outfile:
        outfile.write(ReportWriter(report).to_json())
    print(f'Output written to {report_file}')


def tui(path: Path):
    with open(path, 'r') as file:
        json = file.read()
    report = ReportReader.from_json(json)
    RefactorList(report, Path(get_parent_folder(str(path)))).show()
    click.echo('Have a nice day! 🍀')


if __name__ == '__main__':
    cli()
