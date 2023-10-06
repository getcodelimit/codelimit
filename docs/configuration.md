# Configuration

## Excluding functions

Functions can be excluded from analysis by putting a `# nocl` comment on the
line above the start of the function, or at any line of the function header.

For example, to ignore a function with a `# nocl` comment above the start of
the function:

```python
# nocl
def some_function():
    ...
```

Or you can ignore a function by putting a `# nocl` comment on any line of the
header:

```python
def some_function():  # nocl
    ...
```

```python
def some_functions(
        some_numbers: list[int]
) -> int:  # nocl
    ...
```

## Excluding files

Files can be excluded from analysis by using the `--exclude` option.
This option can be used multiple times and takes a [glob pattern](https://en.wikipedia.org/wiki/Glob_(programming)) as a
value, for example:

```shell
codelimit --exclude "*.generated.py" --exclude "docs/*" ...
```

The `--exclude` option extends the default exclusion list.
The default exclusion list is:

```python
[
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "venv",
    "test",
    "tests",
]
```