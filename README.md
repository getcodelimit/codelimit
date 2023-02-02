# Code Limit

![Logo](docs/codelimit-logo-360x360.png)

[![codecov](https://codecov.io/gh/getcodelimit/codelimit/branch/main/graph/badge.svg?token=ZQBEAJVC2Y)](https://codecov.io/gh/getcodelimit/codelimit)

Build with:
- [Pygments](https://pygments.org)
- [Click](https://click.palletsprojects.com)
- [InquirerPy](https://inquirerpy.readthedocs.io)
- [Plotext](https://github.com/piccolomo/plotext)
- [Textual](https://github.com/Textualize/textual)

# Usage

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
./make-dist.sh
```
