#!/usr/bin/env python3
import os.path
import sys
from pathlib import Path

from codelimit.common.Scanner import scan
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.tui.CodeLimitApp import CodeLimitApp

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not os.path.exists(path):
            print(f'{sys.argv[1]} is not a valid path!')
            sys.exit(1)
    else:
        path = Path('.')
    report_path = os.path.join(path, 'codelimit.json')
    if not os.path.exists(report_path):
        codebase = scan(path)
        codebase.aggregate()
        report = Report(codebase)
        with open(report_path, 'w') as outfile:
            outfile.write(ReportWriter(report).to_json())
    with open(report_path, 'r') as file:
        json = file.read()
    report = ReportReader.from_json(json)
    app = CodeLimitApp(report)
    app.run()
