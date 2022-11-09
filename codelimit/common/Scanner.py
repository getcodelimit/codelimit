import os
from os.path import relpath

from halo import Halo

from codelimit.common.SourceFile import SourceFile
from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.Codebase import Codebase
from codelimit.common.Scope import build_scopes
from codelimit.common.utils import risk_categories
from codelimit.languages.python.Python import get_headers, get_blocks


def is_hidden(root, file):
    if file.startswith('.'):
        return True
    return len([d for d in root.split(os.sep)[1:] if d.startswith('.')]) > 0


def scan(path: str) -> Codebase:
    result = Codebase()
    spinner = Halo(text='Scanning', spinner='dots')
    spinner.start()
    scanned = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if is_hidden(root, file):
                continue
            if file.lower().endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath) as f:
                    code = f.read()
                headers = get_headers(code)
                blocks = get_blocks(code)
                scopes = build_scopes(headers, blocks)
                if scopes:
                    rel_path = relpath(filepath, path)
                    file_measurements = SourceFile(rel_path)
                    measurements = []
                    for scope in scopes:
                        length = scope.block.end.line - scope.header.start.line + 1
                        measurements.append(SourceMeasurement(scope.header.start.line, length))
                    file_measurements.measurements = measurements
                    file_measurements.risk_categories = risk_categories(measurements)
                    result.add(file_measurements)
                scanned += 1
                spinner.text = f'Scanned {scanned} file(s)'
    spinner.succeed()
    return result
