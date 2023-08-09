# CodeLimit

Your Refactoring Alarm

![Logo](docs/codelimit-logo-96x96.png)

![Screenshot](docs/screenshot.png)

[![CI](https://github.com/getcodelimit/codelimit/actions/workflows/ci.yml/badge.svg)](https://github.com/getcodelimit/codelimit/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/getcodelimit/codelimit/branch/main/graph/badge.svg?token=ZQBEAJVC2Y)](https://codecov.io/gh/getcodelimit/codelimit)

# Usage

## Running

After installing depencies with `poetry install`, CodeLimit can be run from the
repository root like this:

```shell
poetry run codelimit
```

For example, to check a codebase at `~/projects/fastapi` run:

```shell
poetry run codelimit ~/projects/fastapi
```

# Development

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
./build-dist.sh
```
