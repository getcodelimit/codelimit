# Standalone Usage

Run Code Limit without arguments to see the usage page:

```shell
$ codelimit

 Usage: codelimit [OPTIONS] COMMAND [ARGS]...

 CodeLimit: Your refactoring alarm.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --verbose  -v            Verbose output                                      │
│ --exclude          TEXT  Glob patterns for exclusion [default: None]         │
│ --version  -V            Show version                                        │
│ --help                   Show this message and exit.                         │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ check          Check file(s)                                                 │
│ scan           Scan a codebase                                               │
│ report         Show report for codebase                                      │
│ app            Code Limit GitHub App commands                                │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Scanning a codebase

To scan a complete codebase and launch the TUI, run:

```shell
codelimit scan path/to/codebase
```

<div id="usage.cast" style="z-index: 1; position: relative;"></div>
<script>
  window.onload = function(){
    AsciinemaPlayer.create('/assets/usage.cast', document.getElementById('usage.cast'));
}
</script>

## Checking files

To check a single file or list of files for functions that need refactoring,
run:

```shell
codelimit check a.py b.py c.py
```
