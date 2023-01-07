#!/usr/bin/env python3
from pathlib import Path

import click
from InquirerPy import inquirer

from codelimit.common.Scanner import Scanner
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportUnit import format_report_unit
from codelimit.common.report.ReportWriter import ReportWriter
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
    units = [format_report_unit(unit) for unit in report.all_report_units_sorted_by_length_asc()]
    inquirer.select(message='Select unit', choices=units).execute()


if __name__ == '__main__':
    cli()
