import fnmatch
import locale
import os
from datetime import datetime
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
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.Token import Token
from codelimit.common.lexer_utils import lex
from codelimit.common.report.Report import Report
from codelimit.common.scope.Scope import count_lines
from codelimit.common.scope.scope_utils import build_scopes, unfold_scopes
from codelimit.common.source_utils import filter_tokens
from codelimit.common.utils import (
    calculate_checksum,
)
from codelimit.languages import Languages
from codelimit.version import version

locale.setlocale(locale.LC_ALL, "")


def scan_codebase(path: Path, cached_report: Union[Report, None] = None) -> Codebase:
    codebase = Codebase(str(path.resolve().absolute()))
    print_header(cached_report, path)
    scan_totals = ScanTotals()
    with Live(refresh_per_second=2) as live:

        def add_file_entry(entry: SourceFileEntry):
            scan_totals.add(entry)
            table = ScanResultTable(scan_totals)
            live.update(table)

        _scan_folder(codebase, path, cached_report, add_file_entry)
        live.stop()
        live.refresh()
    print()
    print_refactor_candidates(scan_totals)
    return codebase


def print_header(cached_report, path):
    print(f"  [bold]Code Limit[/bold]: {version}")
    print(
        f"  [bold]Scan date[/bold]: {datetime.now().isoformat(sep=' ', timespec='seconds')}"
    )
    print(f"  [bold]Scan root[/bold]: {path.resolve().absolute()}")
    if cached_report:
        print("  [bold]Found cached report, only analyzing changed files[/bold]")


def print_refactor_candidates(scan_totals: ScanTotals):
    total_hard_to_maintain = scan_totals.total_hard_to_maintain()
    if total_hard_to_maintain > 0:
        print(
            f"  [dark_orange]\u26A0[/dark_orange] {total_hard_to_maintain} functions are hard-to-maintain."
        )
    total_unmaintainable = scan_totals.total_unmaintainable()
    if total_unmaintainable > 0:
        print(f"  [red]\u2716[/red] {total_unmaintainable} functions need refactoring.")
    if total_hard_to_maintain == 0 and total_unmaintainable == 0:
        print(
            "  [bold]Refactoring not necessary, :glowing_star: happy coding! :glowing_star:[/bold]"
        )


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
                lexer_name = lexer.__class__.name
                file_path = os.path.join(root, file)
                languages = Languages.by_name.keys()
                if lexer_name in languages:
                    file_entry = _scan_file(
                        codebase, lexer, folder, file_path, cached_report
                    )
                    if add_file_entry:
                        add_file_entry(file_entry)
            except ClassNotFound:
                pass


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


def _analyze_file(path, rel_path, checksum, lexer):
    with open(path) as f:
        code = f.read()
    all_tokens = lex(lexer, code, False)
    code_tokens = filter_tokens(all_tokens)
    file_loc = count_lines(code_tokens)
    language_name = lexer.__class__.name
    language = Languages.by_name[language_name]
    if language:
        measurements = scan_file(all_tokens, language)
    else:
        measurements = []
    entry = SourceFileEntry(
        rel_path, checksum, lexer.__class__.name, file_loc, measurements
    )
    return entry


def scan_file(tokens: list[Token], language: Language) -> list[Measurement]:
    scopes = build_scopes(tokens, language)
    scopes = unfold_scopes(scopes)
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
