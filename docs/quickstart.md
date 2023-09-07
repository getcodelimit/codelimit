# Quickstart

Depending on your development workflow, Code Limit can run as:

- [Pre-commit hook](#pre-commit-hook)
- [GitHub Action](#github-action)
- Standalone
    - [Homebrew](#homebrew-install)
    - [Pipx](#pipx-install)
    - [Pypi](#pypi-install)
    - [Platform binary](#platform-binaries)

## Pre-commit hook

Code Limit can be installed as a [pre-commit](https://pre-commit.com/) hook so
it alarms you during development when it's time to refactor:

```yaml
-   repo: https://github.com/getcodelimit/codelimit
    rev: 0.6.2
    hooks:
    - id: codelimit
```

Code Limit is intended to be used alongside formatting, linters and other hooks
that improve the consistency and quality of your code (such as
[Black](https://github.com/psf/black),
[Ruff](https://github.com/astral-sh/ruff) and
[MyPy](https://github.com/python/mypy).) As an example pre-commit configuration
see the
[`pre-commit-config.yaml`](https://github.com/getcodelimit/codelimit/blob/main/.pre-commit-config.yaml)
from Code Limit itself.

When running as a hook, Code Limit *warns* about functions that *should* be
refactored and *fails* for functions that *need* to be refactord.

## GitHub Action

Code Limit is available as a GitHub Action

When running as a GitHub Action, Code Limit only checks modified files and
*warns* about functions that *should* be refactored and *fails* for functions
that *need* to be refactored.

To run Code Limit on every push and before every merge to `main`, append it to
your GH Action workflow:

```yaml
name: 'main'
on:
  push:
    branches: main
  pull_request:
    branches: main
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout'
        uses: actions/checkout@v2
      - name: 'Run Code Limit'
        uses: getcodelimit/codelimit-action@main
```

## Standalone

Code Limit can also run as a standalone program.

### Homebrew install

Code Limit is available on
[Homebrew](https://formulae.brew.sh/formula/codelimit):

```shell
brew install codelimit
```

### Pipx install

To install the standalone version of Code Limit in an isolated Python
environment using [pipx](https://pypa.github.io/pipx) run:

```
pipx install codelimit
```

### PyPi install

To install the standalone version of Code Limit for your default Python
installation run:

```shell
python -m pip install codelimit
```

### Platform binaries

Binaries for different platforms (macOS, Linux, Windows) are available on the
[latest release
page](https://github.com/getcodelimit/codelimit/releases/latest).

