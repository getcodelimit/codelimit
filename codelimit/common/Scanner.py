import locale
import logging
import os
from os.path import relpath
from pathlib import Path
from typing import Union, Callable

from pathspec import PathSpec
from pygments.lexer import Lexer
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from rich.live import Live
from rich import print

from codelimit.common.Codebase import Codebase
from codelimit.common.Configuration import Configuration
from codelimit.common.Language import Language
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.ScanResultTable import ScanResultTable
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.Token import Token
from codelimit.common.lexer_utils import lex
from codelimit.common.report.Report import Report
from codelimit.common.scope.scope_utils import build_scopes, unfold_scopes, count_lines
from codelimit.common.source_utils import filter_tokens
from codelimit.common.utils import (
    calculate_checksum,
)
from codelimit.languages import Languages

locale.setlocale(locale.LC_ALL, "")


def scan_codebase(path: Path, cached_report: Union[Report, None] = None) -> Codebase:
    scan_totals = ScanTotals()
    if Configuration.verbose:
        def add_file_entry(entry: SourceFileEntry):
            scan_totals.add(entry)

        codebase = scan_path(path, cached_report, add_file_entry)
        print(ScanResultTable(scan_totals))
    else:
        with Live(refresh_per_second=2) as live:
            def add_file_entry(entry: SourceFileEntry):
                scan_totals.add(entry)
                table = ScanResultTable(scan_totals)
                live.update(table)

            codebase = scan_path(path, cached_report, add_file_entry)
            live.stop()
            live.refresh()
    return codebase


def scan_path(path: Path, cached_report: Union[Report, None] = None,
              add_file_entry_callback: Union[Callable[[SourceFileEntry], None], None] = None,
              ) -> Codebase:
    result = Codebase(str(path.resolve().absolute()))
    excludes_spec = generate_exclude_spec(path)
    for root, dirs, files in os.walk(path.absolute()):
        files = [f for f in files if not f[0] == "."]
        dirs[:] = [d for d in dirs if not d[0] == "."]
        for file in files:
            rel_path = Path(os.path.join(root, file)).relative_to(path.absolute())
            if is_excluded(rel_path, excludes_spec):
                continue
            try:
                lexer = get_lexer_for_filename(rel_path)
                lexer_name = lexer.__class__.name
                file_path = os.path.join(root, file)
                languages = Languages.by_name.keys()
                if lexer_name in languages:
                    file_entry = _scan_file(
                        result, lexer, path, file_path, cached_report
                    )
                    if add_file_entry_callback:
                        add_file_entry_callback(file_entry)
            except ClassNotFound:
                pass
    return result


def _scan_file(
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
    else:
        entry = _analyze_file(path, rel_path, checksum, lexer)
    codebase.add_file(entry)
    return entry


def _read_file(path: Path):
    try:
        with open(path) as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, encoding="latin-1") as f:
            return f.read()


def _analyze_file(path, rel_path, checksum, lexer):
    logging.info(f"Analyzing {rel_path}")
    code = _read_file(path)
    all_tokens = lex(lexer, code, False)
    language_name = lexer.__class__.name
    language = Languages.by_name[language_name]
    if language:
        measurements = scan_file(all_tokens, language)
    else:
        measurements = []
    file_loc = sum([m.value for m in measurements])
    entry = SourceFileEntry(
        rel_path, checksum, lexer.__class__.name, file_loc, measurements
    )
    return entry


def scan_file(tokens: list[Token], language: Language) -> list[Measurement]:
    scopes = build_scopes(tokens, language)
    scopes = unfold_scopes(scopes)
    measurements: list[Measurement] = []
    code_tokens = filter_tokens(tokens)
    if scopes:
        for scope in scopes:
            length = count_lines(scope, code_tokens)
            start_location = code_tokens[scope.header.token_range.start].location
            last_token = code_tokens[scope.block.end - 1]
            end_location = Location(
                last_token.location.line,
                last_token.location.column + len(last_token.value),
            )
            measurements.append(
                Measurement(scope.header.name, start_location, end_location, length)
            )
    return measurements


def generate_exclude_spec(root: Path) -> PathSpec:
    excludes = DEFAULT_EXCLUDES.copy()
    excludes.extend(Configuration.exclude)
    gitignore_excludes = _read_gitignore(root)
    if gitignore_excludes:
        excludes.extend(gitignore_excludes)
    return PathSpec.from_lines("gitignore", excludes)


def _read_gitignore(path: Path) -> list[str] | None:
    gitignore_path = path.joinpath(".gitignore")
    if gitignore_path.exists():
        return gitignore_path.read_text().splitlines()
    return None


def is_excluded(path: Path, spec: PathSpec):
    return spec.match_file(path)


DEFAULT_EXCLUDES = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "venv",
    "test",
    "tests",
]
