import fnmatch
import os
from os.path import relpath
from pathlib import Path
from typing import Union

from halo import Halo
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

from codelimit.common.Codebase import Codebase
from codelimit.common.Configuration import Configuration
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.Token import Token
from codelimit.common.lexer_utils import lex
from codelimit.common.report.Report import Report
from codelimit.common.scope.Scope import count_lines
from codelimit.common.scope.ScopeExtractor import ScopeExtractor
from codelimit.common.scope.scope_extractor_utils import build_scopes
from codelimit.common.source_utils import filter_tokens
from codelimit.common.utils import calculate_checksum, load_scope_extractor_by_name

languages = ["JavaScript", "Python"]

ignored = ["CSS", "HTML", "JSON", "Markdown", "Text only", "TOML", "XML", "YAML"]


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
            try:
                lexer = get_lexer_for_filename(rel_path)
                language = lexer.__class__.name
                if language in languages:
                    file_path = os.path.join(root, file)
                    _add_file(codebase, lexer, folder, file_path, cached_report)
                    scanned += 1
                    spinner.text = f"Scanned {scanned} file(s)"
                elif language in ignored:
                    pass
                else:
                    print(f"Unclassified: {language}")
            except ClassNotFound:
                pass
    spinner.succeed()


def _add_file(
    codebase: Codebase,
    lexer: Lexer,
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
            SourceFileEntry(
                rel_path,
                checksum,
                cached_entry.language,
                cached_entry.loc,
                cached_entry.measurements(),
            )
        )
    else:
        with open(path) as f:
            code = f.read()
        all_tokens = lex(lexer, code, False)
        code_tokens = filter_tokens(all_tokens)
        file_loc = count_lines(code_tokens)
        scope_extractor = load_scope_extractor_by_name(lexer.__class__.name)
        if scope_extractor:
            measurements = scan_file(all_tokens, scope_extractor)
        else:
            measurements = []
        codebase.add_file(
            SourceFileEntry(
                rel_path, checksum, lexer.__class__.name, file_loc, measurements
            )
        )


def scan_file(
    tokens: list[Token], scope_extractor: ScopeExtractor
) -> list[Measurement]:
    scopes = build_scopes(tokens, scope_extractor)
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
