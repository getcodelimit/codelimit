# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Code Limit ("Your Refactoring Alarm") is a Python CLI that measures function length (lines of code per function) across
a codebase and flags functions that are getting too long to maintain. User docs live at https://getcodelimit.github.io
(not in this repo).

## Commands

The project uses `uv`. CI runs on Python 3.10 and 3.14 (`requires-python = ">=3.10,<3.15"`).

```bash
uv sync --dev                          # install deps
uv run pytest                          # all unit tests
uv run pytest tests/languages/test_Java.py::test_function_with_throws   # single test
uv run pytest --cov --cov-report=xml   # with coverage (as CI does)
uv run ruff check .                    # lint (CI, on PRs)
uv run mypy codelimit/                 # type check (CI, on PRs)
uv run codelimit scan .                # run the CLI on this repo (also: report, findings, check, badge)
uv run poe bundle                      # pyinstaller binary
uv run poe regression run [examples/<dir>]   # regression runner (clones real repos; slow, network)
uv run python tests/regression.py add <owner/repo> <tag>   # add a regression example
```

## Architecture

**Pipeline:** file → Pygments lexer → tokens → language-specific *headers* (function signatures) and *blocks* (bodies) →
*scopes* (header + block) → `Measurement` (name, start/end location, line count).

- `codelimit/__main__.py` — Typer CLI (`scan`, `report`, `findings`, `check`, `badge`). Each command calls
  `Configuration.load(path)` (reads `.codelimit.yml`: `exclude`, `verbose`) and then dispatches to
  `codelimit/commands/*.py`. `Configuration` is global class-level state.
- `codelimit/common/Scanner.py` — walks the tree, skips dotfiles/dirs, applies excludes (`DEFAULT_EXCLUDES` + config +
  root `.gitignore`, via `pathspec`; note that `test`/`tests` dirs are excluded by default), picks a lexer with
  `get_lexer_for_filename`, and runs `scan_file`. `scan` writes a JSON report to `.codelimit_cache/codelimit.json` and
  reuses unchanged-file entries on later runs (keyed by checksum; the cache is ignored when `Report.VERSION` changes).
  `report`/`findings` read that cached report.
- `codelimit/commands/check.py` — pre-commit hook entry (`codelimit check --quiet`, see `.pre-commit-hooks.yaml`). It
  exits 1 when any function is longer than 60 lines.
- **Risk thresholds** (≤15 / ≤30 / ≤60 / >60 lines) are hardcoded in several places in `codelimit/common/utils.py` and
  `commands/check.py`.

### Languages

- Each language is a `Language` subclass in `codelimit/languages/` that implements `extract_headers(tokens)` and
  `extract_blocks(tokens, headers)`. `Languages.by_name` is built automatically from `Language.__subclasses__()`, and
  the scanner matches it against the **Pygments lexer name**. So `Language.name` must match the lexer's `name` exactly,
  and a new language must be imported in `codelimit/languages/__init__.py`.
- Brace languages use `scope_utils.get_blocks(tokens, "{", "}")`. Python uses indentation-based block detection.
- `allow_nested_functions=False` drops nested scopes instead of folding them into their parent as children.
- Functions preceded by a `# nocl` / `// nocl` comment are excluded (`source_utils.filter_nocl_comment_tokens`).

### Token pattern matching (`codelimit/common/gsm/`)

Headers are found with a small in-house regex engine over token sequences: expressions are lists of predicates and
operators (`OneOrMore`, `ZeroOrMore`, `Optional`, `Union`), which are compiled NFA → DFA (`gsm/Expression.py`,
`gsm/automata/`) and matched with `gsm/matcher.py` (`find_all`, `starts_with`). Token predicates (`Keyword`, `Name`,
`Symbol`, `Balanced`, `And`/`Or`/`Not`, …) live in `common/token_matching/predicate/`.
`scope_utils.get_headers(tokens, expression, followed_by=..., nested=...)` is the usual entry point. See
`languages/Java.py` for an example.

## Testing

- Language tests use `tests/conftest.py::assert_functions(code, Languages.X, {"func_name": line_count})`, which asserts
  the exact set of detected functions and their lengths.
- `examples/<owner>_<repo>_<tag>/codelimit.json` are reference reports for real open-source repos. The regression
  workflow (self-hosted runner) re-scans them and fails if the per-language totals change, and it overwrites the stored
  report when they do. If a parser change is intended, regenerate the affected examples and commit them.

## Conventions

- Commits use Conventional Commits with a gitmoji, e.g. `feat: ✨ ...`, `fix: 🐛 ...`, `fix: 🩹 ...`, `ci: 👷 ...`,
  `chore: 🚧 ...`. Releases are cut by python-semantic-release (manual `release` workflow), which bumps `pyproject.toml`
  and `codelimit/version.py` together. Don't bump versions by hand.
