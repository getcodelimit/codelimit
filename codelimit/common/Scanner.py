import os
from os.path import relpath

from halo import Halo

from codelimit.common.Measurement import Measurement
from codelimit.common.Measurements import Measurements
from codelimit.common.Scope import build_scopes
from codelimit.languages.python.Python import get_headers, get_blocks


def is_hidden(root, file):
    if file.startswith('.'):
        return True
    return len([d for d in root.split(os.sep)[1:] if d.startswith('.')]) > 0


def scan(path: str) -> Measurements:
    result = Measurements()
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
                for scope in scopes:
                    length = scope.block.end.line - scope.header.start.line + 1
                    rel_path = relpath(filepath, path)
                    measurement = Measurement(rel_path, scope.header.start.line, length)
                    result.add(measurement)
                scanned += 1
                spinner.text = f'Scanned {scanned} file(s)'
    spinner.succeed()
    return result
