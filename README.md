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

## Installation

CodeLimit can be installed as a [pre-commit](https://pre-commit.com/) hook so
it alarms you during development when it's time to refactor:

```yaml
-   repo: https://github.com/getcodelimit/codelimit
    rev: v0.2.1
    hooks:
    - id: codelimit
```

CodeLimit is intended to be used alongside formatting, linters and other hooks
that improve the consistency and quality of your code (such as Black, Ruff and
MyPy.) As an example pre-commit configuration see the
[`pre-commit-config.yaml`](https://github.com/getcodelimit/codelimit/blob/main/.pre-commit-config.yaml)
from CodeLimit itself.

When running as a hook, CodeLimit *warns* about functions that *should* be
refactored and *fails* for functions that *need* to be refactord.

To show your project uses CodeLimit place this badge in the README markdown:
```
![Checked with CodeLimit](https://img.shields.io/badge/CodeLimit-checked-green.svg)](https://github.com/getcodelimit/codelimit)
```

## Standalone

![Screenshot](https://github.com/getcodelimit/codelimit/blob/main/docs/screenshot.png)

To install the standalone version of CodeLimit for your default Python
installation run:

```shell
python -m pip install codelimit
```

# Development

After installing depencies with `poetry install`, CodeLimit can be run from the
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
