import os
from os.path import relpath
from pathlib import Path

from halo import Halo

from codelimit.common.Codebase import Codebase
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.scope.scope_utils import build_scopes
from codelimit.common.utils import calculate_checksum
from codelimit.languages.c.CLanguage import CLanguage
from codelimit.languages.python.PythonLaguage import PythonLanguage


class Scanner:

    def __init__(self):
        self.languages = [PythonLanguage(), CLanguage()]
        self.codebase = Codebase()

    def scan(self, path: Path) -> Codebase:
        if path.is_dir():
            return self._scan_folder(path)
        else:
            for language in self.languages:
                if language.accept_file(str(path)):
                    self._scan_file(language, path.parent, str(path))
        return self.codebase

    def _scan_folder(self, folder: Path) -> Codebase:
        spinner = Halo(text='Scanning', spinner='dots')
        spinner.start()
        scanned = 0
        for root, dirs, files in os.walk(folder.absolute()):
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            for file in files:
                for language in self.languages:
                    file_path = os.path.join(root, file)
                    if language.accept_file(file_path):
                        self._scan_file(language, folder, file_path)
                        scanned += 1
                        spinner.text = f'Scanned {scanned} file(s)'
        spinner.succeed()
        return self.codebase

    def _scan_file(self, language, root: Path, path):
        rel_path = relpath(path, root)
        with open(path) as f:
            code = f.read()
        scopes = build_scopes(language, code)
        if scopes:
            measurements = []
            for scope in scopes:
                length = len(scope)
                start_location = scope.header.token_range[0].location
                last_token = scope.block.tokens[-1]
                end_location = Location(last_token.location.line,
                                        last_token.location.column + len(last_token.value))
                measurements.append(Measurement(scope.header.name, start_location, end_location, length))
            checksum = calculate_checksum(path)
            self.codebase.add_file(SourceFileEntry(rel_path, checksum, measurements))
