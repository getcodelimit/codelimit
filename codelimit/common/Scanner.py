import fnmatch
import os
from os.path import relpath
from pathlib import Path
from typing import Union

from halo import Halo

from codelimit.common.Codebase import Codebase
from codelimit.common.Configuration import Configuration
from codelimit.common.Language import Language
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.report.Report import Report
from codelimit.common.scope.scope_utils import build_scopes
from codelimit.common.utils import calculate_checksum
from codelimit.languages.python.PythonLanguage import PythonLanguage

languages = [
    PythonLanguage()
]  # , CLanguage(), JavaScriptLanguage(), TypeScriptLanguage()]


def scan_codebase(path: Path, cached_report: Union[Report, None] = None) -> Codebase:
    codebase = Codebase(str(path.absolute()))
    _scan_folder(codebase, path, cached_report)
    return codebase


def _scan_folder(
    codebase: Codebase, folder: Path, cached_report: Union[Report, None] = None
):
    spinner = Halo(text="Scanning", spinner="dots")
    spinner.start()
    scanned = 0
    for root, dirs, files in os.walk(folder.absolute()):
        files = [f for f in files if not f[0] == "."]
        dirs[:] = [d for d in dirs if not d[0] == "."]
        for file in files:
            rel_path = Path(os.path.join(root, file)).relative_to(folder.absolute())
            if is_excluded(rel_path):
                continue
            for language in languages:
                file_path = os.path.join(root, file)
                if language.accept_file(file_path):
                    _add_file(codebase, language, folder, file_path, cached_report)
                    scanned += 1
                    spinner.text = f"Scanned {scanned} file(s)"
    spinner.succeed()


def _add_file(
    codebase: Codebase,
    language,
    root: Path,
    path: str,
    cached_report: Union[Report, None] = None,
):
    checksum = calculate_checksum(path)
    rel_path = relpath(path, root)
    cached_entry = None
    if cached_report:
        rel_path = relpath(path, root)
        try:
            cached_entry = cached_report.codebase.files[rel_path]
        except KeyError:
            pass
    if cached_entry and cached_entry.checksum() == checksum:
        codebase.add_file(
            SourceFileEntry(rel_path, checksum, cached_entry.measurements())
        )
    else:
        measurements = scan_file(language, path)
        if measurements:
            codebase.add_file(SourceFileEntry(rel_path, checksum, measurements))


def scan_file(language: Language, path: str) -> list[Measurement]:
    with open(path) as f:
        code = f.read()
    scopes = build_scopes(language, code)
    measurements: list[Measurement] = []
    if scopes:
        for scope in scopes:
            length = len(scope)
            start_location = scope.header.token_range[0].location
            last_token = scope.block.tokens[-1]
            end_location = Location(
                last_token.location.line,
                last_token.location.column + len(last_token.value),
            )
            measurements.append(
                Measurement(scope.header.name, start_location, end_location, length)
            )
    return measurements


def is_excluded(path: Path):
    for exclude in Configuration.excludes:
        exclude_parts = exclude.split(os.sep)
        if len(exclude_parts) == 1:
            for part in path.parts:
                if fnmatch.fnmatch(part, exclude):
                    return True
        else:
            if fnmatch.fnmatch(str(path), exclude):
                return True
    return False
