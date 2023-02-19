#!/usr/bin/env python3
import os.path
from pathlib import Path

from codelimit.common.Scanner import scan
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportWriter import ReportWriter
from codelimit.tui.CodeLimitApp import CodeLimitApp

app = CodeLimitApp()

if __name__ == '__main__':
    if not os.path.exists('codelimit.json'):
        codebase = scan(Path('.'))
        codebase.aggregate()
        report = Report(codebase)
        with open('codelimit.json', 'w') as outfile:
            outfile.write(ReportWriter(report).to_json())
    app.run()
