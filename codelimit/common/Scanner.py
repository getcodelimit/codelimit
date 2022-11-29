import os
from os.path import relpath
from pathlib import Path

from halo import Halo

from codelimit.common.Codebase import Codebase
from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.scope_utils import build_scopes
from codelimit.languages.c.CLanguage import CLanguage
from codelimit.languages.python.PythonLaguage import PythonLanguage


class Scanner:

    def __init__(self):
        self.languages = [PythonLanguage(), CLanguage()]
        self.codebase = Codebase()

    def scan(self, path: Path) -> Codebase:
        if path.is_dir():
            return self._scan_dir(path)
        else:
            for language in self.languages:
                if language.accept_file(str(path)):
                    self._scan_file(language, path, str(path.parent), str(path))
        return self.codebase

    def _scan_dir(self, path: Path) -> Codebase:
        spinner = Halo(text='Scanning', spinner='dots')
        spinner.start()
        scanned = 0
        for root, dirs, files in os.walk(path.absolute()):
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            for file in files:
                for language in self.languages:
                    if language.accept_file(file):
                        self._scan_file(language, path, root, file)
                        scanned += 1
                        spinner.text = f'Scanned {scanned} file(s)'
        spinner.succeed()
        return self.codebase

    def _scan_file(self, language, root, folder, file):
        filepath = os.path.join(folder, file)
        rel_path = relpath(filepath, root)
        with open(filepath) as f:
            code = f.read()
        scopes = build_scopes(language, code)
        if scopes:
            measurements = []
            for scope in scopes:
                length = len(scope)
                measurements.append(SourceMeasurement(scope.header.tokens[0].location.line, length))
            self.codebase.add_file(rel_path, measurements)
