# Configuration

## Ignoring functions

Functions can be excluded from analysis by putting a `# nocl` comment on the
line above the start of the funtion, or any line of the function header.

For example, to ignore a function with a `# nocl` comment above the start of
the funtions:

```python
# nocl
def some_function():
    ...
```

Or you can ignore a function by putting a `# nocl` comment on any line of the
header:

```python
def some_function(): # nocl
    ...
```

```python
def some_functions(
        some_numbers: list[int]
) -> int: # nocl
    ...
```
