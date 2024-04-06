# Development

After installing dependencies with `poetry install`, Code Limit can be run from the
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

## Static documentation

Generating the static documentation:

```shell
poetry run mkdocs build
```

See the output:

```shell
poetry run mkdocs serve
```

Terminal sessions in the documentation are recorded with the [Asciinema
CLI](https://docs.asciinema.org/getting-started/) and stored in the `assets`
folder:

```shell
asciinema rec scan.cast
```
