import os
from pathlib import Path

import typer
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound

from codelimit.common.CheckResult import CheckResult
from codelimit.common.Scanner import is_excluded, scan_file
from codelimit.common.lexer_utils import lex
from codelimit.languages import Languages


def check_command(paths: list[Path], quiet: bool):
    check_result = CheckResult()
    for path in paths:
        if path.is_file():
            check_file(path, check_result)
        elif path.is_dir():
            for root, dirs, files in os.walk(path.absolute()):
                files = [f for f in files if not f[0] == "."]
                dirs[:] = [d for d in dirs if not d[0] == "."]
                for file in files:
                    abs_path = Path(os.path.join(root, file))
                    rel_path = abs_path.relative_to(path.absolute())
                    if is_excluded(rel_path):
                        continue
                    check_file(abs_path, check_result)
    exit_code = 1 if check_result.unmaintainable > 0 else 0
    if (
        not quiet
        or check_result.hard_to_maintain > 0
        or check_result.unmaintainable > 0
    ):
        check_result.report()
    raise typer.Exit(code=exit_code)


def check_file(path: Path, check_result: CheckResult):
    try:
        lexer = get_lexer_for_filename(path)
    except ClassNotFound:
        return
    lexer_name = lexer.__class__.name
    if lexer_name in Languages.by_name.keys():
        with open(path) as f:
            code = f.read()
        tokens = lex(lexer, code, False)
        lexer_name = Languages.by_name[lexer.__class__.name]
        if lexer_name:
            measurements = scan_file(tokens, lexer_name)
            risks = sorted(
                [m for m in measurements if m.value > 30],
                key=lambda measurement: measurement.value,
                reverse=True,
            )
            check_result.add(path, risks)
