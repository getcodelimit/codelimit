#!/usr/bin/env python3
from codelimit.Scanner import scan
from codelimit.version import version, release_date

print('Code Limit')
print(f'Version: {version}, released on: {release_date}')

report = scan('.')
print(f'Total lines of code: {report.total_lines_of_code}')
print(f'Average length (LOC): {report.get_average()}')
print(f'90th percentile: {report.ninetieth_percentile()}')