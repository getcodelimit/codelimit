import os
from os.path import relpath
from pathlib import Path

from halo import Halo

from codelimit.common.Codebase import Codebase
from codelimit.common.SourceFile import SourceFile
from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.scope_utils import build_scopes
from codelimit.common.utils import risk_categories
from codelimit.common.Language import Language
from codelimit.languages.python.PythonLaguage import PythonLanguage


def scan(path: Path) -> Codebase:
    print(path.absolute())
    language: Language = PythonLanguage()
    result = Codebase()
    spinner = Halo(text='Scanning', spinner='dots')
    spinner.start()
    scanned = 0
    for root, dirs, files in os.walk(path.absolute()):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            filepath = os.path.join(root, file)
            if language.accept_file(filepath):
                with open(filepath) as f:
                    code = f.read()
                scopes = build_scopes(language, code)
                if scopes:
                    rel_path = relpath(filepath, path)
                    file_measurements = SourceFile(rel_path)
                    measurements = []
                    for scope in scopes:
                        length = len(scope)
                        measurements.append(SourceMeasurement(scope.header.tokens[0].location.line, length))
                    file_measurements.measurements = measurements
                    file_measurements.risk_categories = risk_categories(measurements)
                    result.add(file_measurements)
                scanned += 1
                spinner.text = f'Scanned {scanned} file(s)'
    spinner.succeed()
    return result
