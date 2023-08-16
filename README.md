# CodeLimit

Your Refactoring Alarm

![Logo](https://raw.githubusercontent.com/getcodelimit/codelimit/main/docs/codelimit-logo-96x96.png)

[![CI](https://github.com/getcodelimit/codelimit/actions/workflows/ci.yml/badge.svg)](https://github.com/getcodelimit/codelimit/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/getcodelimit/codelimit/branch/main/graph/badge.svg?token=ZQBEAJVC2Y)](https://codecov.io/gh/getcodelimit/codelimit)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with CodeLimit](https://img.shields.io/badge/CodeLimit-checked-green.svg)](https://github.com/getcodelimit/codelimit)

# Quickstart

## Pre-commit hook

CodeLimit can be installed as a [pre-commit](https://pre-commit.com/) hook so
it alarms you during development when it's time to refactor:

```yaml
-   repo: https://github.com/getcodelimit/codelimit
    rev: v0.3.0
    hooks:
    - id: codelimit
```

CodeLimit is intended to be used alongside formatting, linters and other hooks
that improve the consistency and quality of your code (such as
[Black](https://github.com/psf/black),
[Ruff](https://github.com/astral-sh/ruff) and
[MyPy](https://github.com/python/mypy).) As an example pre-commit configuration
see the
[`pre-commit-config.yaml`](https://github.com/getcodelimit/codelimit/blob/main/.pre-commit-config.yaml)
from CodeLimit itself.

When running as a hook, CodeLimit *warns* about functions that *should* be
refactored and *fails* for functions that *need* to be refactord.

To show your project uses CodeLimit place this badge in the README markdown:
```
![Checked with CodeLimit](https://img.shields.io/badge/CodeLimit-checked-green.svg)](https://github.com/getcodelimit/codelimit)
```

## Standalone

CodeLimit can also run as a standalone program. To install the standalone
version of CodeLimit for your default Python installation run:

```shell
python -m pip install codelimit
```

Run CodeLimit without arguments to see the usage page:

```shell
$ codelimit

 Usage: codelimit [OPTIONS] COMMAND [ARGS]...

 CodeLimit: Your refactoring alarm

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ check                 Check file(s)                                          │
│ scan                  Scan a codebase                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Scanning a codebase

To scan a complete codebase and launch the TUI, run:

```shell
codelimit scan path/to/codebase
```

![Screenshot](https://github.com/getcodelimit/codelimit/blob/main/docs/screenshot.png)

## Checking files

To check a single file or list of files for functions that need refactoring,
run:

```shell
codelimit check a.py b.py c.py
```

# Development

After installing dependencies with `poetry install`, CodeLimit can be run from the
repository root like this:

```shell
poetry run codelimit
```

For example, to check a codebase at `~/projects/fastapi` run:

```shell
poetry run codelimit ~/projects/fastapi
```

## Using the Textal debug console

Open a terminal and start the Textual debug console:

```shell
poetry run textual console
```

Next, open another terminal and start Code Limit in development mode:

```shell
poetry run textual run --dev main.py
```

## Building the binary distribution

Generate a self-contained binary:

```shell
poetry run poe bundle
```
