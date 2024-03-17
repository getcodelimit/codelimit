import fnmatch
import locale
import os
from os.path import relpath
from pathlib import Path
from typing import Union, Callable

from pathspec import PathSpec
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from rich import print
from rich.live import Live

from codelimit.common.Codebase import Codebase
from codelimit.common.Configuration import Configuration
from codelimit.common.Language import Language
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.ScanResultTable import ScanResultTable
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.Token import Token
from codelimit.common.lexer_utils import lex
from codelimit.common.report.Report import Report
from codelimit.common.scope.Scope import count_lines
from codelimit.common.scope.scope_utils import build_scopes
from codelimit.common.source_utils import filter_tokens
from codelimit.common.utils import (
    calculate_checksum,
    make_count_profile,
    load_language_by_name,
)
from codelimit.languages import ignored, LanguageName

locale.setlocale(locale.LC_ALL, "")


def scan_codebase(path: Path, cached_report: Union[Report, None] = None) -> Codebase:
    codebase = Codebase(str(path.absolute()))
    print(f"  [bold]Directory[/bold]: {path.name}")
    with Live() as live:
        languages_totals = {}

        def add_file_entry(entry: SourceFileEntry):
            profile = make_count_profile(entry.measurements())
            if entry.language not in languages_totals:
                languages_totals[entry.language] = {
                    "files": 1,
                    "loc": entry.loc,
                    "functions": len(entry.measurements()),
                    "hard-to-maintain": profile[2],
                    "unmaintainable": profile[2],
                }
            else:
                language_entry = languages_totals[entry.language]
                language_entry["files"] += 1
                language_entry["loc"] += entry.loc
                language_entry["functions"] += len(entry.measurements())
                language_entry["hard-to-maintain"] += profile[2]
                language_entry["unmaintainable"] += profile[3]
            table = ScanResultTable(languages_totals)
            live.update(table)

        _scan_folder(codebase, path, cached_report, add_file_entry)
    total_loc = sum([entry["loc"] for entry in languages_totals.values()])
    print(f"  [bold]Total lines of code[/bold]: {total_loc:n}")
    return codebase


def _scan_folder(
        codebase: Codebase,
        folder: Path,
        cached_report: Union[Report, None] = None,
        add_file_entry: Union[Callable[[SourceFileEntry], None], None] = None,
):
    gitignore = _read_gitignore(folder)
    for root, dirs, files in os.walk(folder.absolute()):
        files = [f for f in files if not f[0] == "."]
        dirs[:] = [d for d in dirs if not d[0] == "."]
        for file in files:
            rel_path = Path(os.path.join(root, file)).relative_to(folder.absolute())
            if is_excluded(rel_path) or (
                    gitignore is not None and is_excluded_by_gitignore(rel_path, gitignore)
            ):
                continue
            try:
                lexer = get_lexer_for_filename(rel_path)
                language = lexer.__class__.name
                file_path = os.path.join(root, file)
                if language in LanguageName:
                    file_entry = _add_file(
                        codebase, lexer, folder, file_path, cached_report
                    )
                    if add_file_entry:
                        add_file_entry(file_entry)
                elif language in ignored:
                    pass
                else:
                    print(f"Unclassified: {language} ({file_path})")
            except ClassNotFound:
                pass


def _add_file(
        codebase: Codebase,
        lexer: Lexer,
        root: Path,
        path: str,
        cached_report: Union[Report, None] = None,
) -> SourceFileEntry:
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
        entry = SourceFileEntry(
            rel_path,
            checksum,
            cached_entry.language,
            cached_entry.loc,
            cached_entry.measurements(),
        )
        codebase.add_file(entry)
        return entry
    else:
        with open(path) as f:
            code = f.read()
        all_tokens = lex(lexer, code, False)
        code_tokens = filter_tokens(all_tokens)
        file_loc = count_lines(code_tokens)
        language_name = lexer.__class__.name
        language = load_language_by_name(language_name)
        if language:
            measurements = scan_file(all_tokens, language)
        else:
            measurements = []
        entry = SourceFileEntry(
            rel_path, checksum, lexer.__class__.name, file_loc, measurements
        )
        codebase.add_file(entry)
        return entry


def scan_file(tokens: list[Token], language: Language) -> list[Measurement]:
    scopes = build_scopes(tokens, language)
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


def _read_gitignore(path: Path) -> PathSpec | None:
    gitignore_path = path.joinpath(".gitignore")
    if gitignore_path.exists():
        return PathSpec.from_lines("gitignore", gitignore_path.read_text().splitlines())
    return None


def is_excluded_by_gitignore(path: Path, gitignore: PathSpec):
    return gitignore.match_file(path)
