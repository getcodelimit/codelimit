# Code Limit

![Logo](docs/codelimit-logo-96x96.png)

![Screenshot](docs/screenshot.png)

[![codecov](https://codecov.io/gh/getcodelimit/codelimit/branch/main/graph/badge.svg?token=ZQBEAJVC2Y)](https://codecov.io/gh/getcodelimit/codelimit)

Build with:
- [Pygments](https://pygments.org)
- [Textual](https://github.com/Textualize/textual)

# Usage

## Running

```shell
poetry run ./main.py [<codebase root path>]
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
