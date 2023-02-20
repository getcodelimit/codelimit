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
from codelimit.languages.javascript.JavaScriptLanguage import JavaScriptLanguage
from codelimit.languages.python.PythonLaguage import PythonLanguage
from codelimit.languages.typescript.TypeScriptLanguage import TypeScriptLanguage

languages = [PythonLanguage(), CLanguage(), JavaScriptLanguage(), TypeScriptLanguage()]


def scan(path: Path) -> Codebase:
    codebase = Codebase(str(path.absolute()))
    _scan_folder(codebase, path)
    return codebase


def _scan_folder(codebase: Codebase, folder: Path):
    spinner = Halo(text='Scanning', spinner='dots')
    spinner.start()
    scanned = 0
    for root, dirs, files in os.walk(folder.absolute()):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            for language in languages:
                file_path = os.path.join(root, file)
                if language.accept_file(file_path):
                    _scan_file(codebase, language, folder, file_path)
                    scanned += 1
                    spinner.text = f'Scanned {scanned} file(s)'
    spinner.succeed()


def _scan_file(codebase: Codebase, language, root: Path, path):
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
        codebase.add_file(SourceFileEntry(rel_path, checksum, measurements))
