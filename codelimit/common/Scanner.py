import os

from halo import Halo

from codelimit.languages.python.Python import get_headers, get_blocks
from codelimit.common.Report import Report, Measurement
from codelimit.common.Scope import build_scopes


def is_hidden(root, file):
    if file.startswith('.'):
        return True
    return len([d for d in root.split(os.sep)[1:] if d.startswith('.')]) > 0


def scan(path: str) -> Report:
    report = Report()
    spinner = Halo(text='Scanning', spinner='dots')
    spinner.start()
    scanned = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if is_hidden(root, file):
                continue
            if file.lower().endswith('.py'):
                with open(os.path.join(root, file)) as f:
                    code = f.read()
                headers = get_headers(code)
                blocks = get_blocks(code)
                scopes = build_scopes(headers, blocks)
                for scope in scopes:
                    length = scope.block.end.line - scope.block.start.line + 1
                    measurement = Measurement(file, scope.header.start.line, length)
                    report.add_measurement(measurement)
                scanned += 1
                spinner.text = f'Scanned {scanned} file(s)'
    spinner.succeed()
    return report
