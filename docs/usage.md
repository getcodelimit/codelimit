# Standalone Usage

Run Code Limit without arguments to see the usage page:

```shell
$ codelimit

 Usage: codelimit [OPTIONS] COMMAND [ARGS]...

 Code Limit: Your refactoring alarm

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

![Screenshot](https://raw.githubusercontent.com/getcodelimit/codelimit/main/docs/assets/screenshot.png)

## Checking files

To check a single file or list of files for functions that need refactoring,
run:

```shell
codelimit check a.py b.py c.py
```
