#!/usr/bin/env python3
from pathlib import Path

import click
from InquirerPy import inquirer

from codelimit.common.Report import Report
from codelimit.common.ReportReader import ReportReader
from codelimit.common.ReportWriter import ReportWriter
from codelimit.common.Scanner import Scanner
from codelimit.version import version, release_date


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path), default='.')
def scan(path: Path):
    print('Code Limit')
    print(f'Version: {version}, released on: {release_date}')

    codebase = Scanner().scan(path)
    codebase.aggregate()
    print(f'Total lines of code: {codebase.total_loc()}')
    report = Report(codebase)
    print(f'Average length (LOC): {report.get_average()}')
    print(f'90th percentile: {report.ninetieth_percentile()}')
    report.display_risk_category_plot()
    with open('codelimit.json', 'w') as outfile:
        outfile.write(ReportWriter(report).to_json())
    print('Output written to codelimit.json')


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
                default='codelimit.json')
def show(path: Path):
    with open(path, 'r') as file:
        json = file.read()
    report = ReportReader.from_json(json)
    folders = [entry.name for entry in report.codebase.tree['./'].entries if entry.is_folder()]
    inquirer.select(message='Select folder', choices=folders).execute()


if __name__ == '__main__':
    cli()
