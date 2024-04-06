import hashlib
import importlib
import os
import sys
from math import ceil
from typing import Union, Any

from rich.style import Style
from rich.text import Text

from codelimit.common.Language import Language
from codelimit.common.Measurement import Measurement
from codelimit.common.gsm.Expression import Expression
from codelimit.common.gsm.operator.Operator import Operator
from codelimit.common.token_matching.predicate.TokenValue import TokenValue


def make_profile(measurements: list[Measurement]):
    result = [0, 0, 0, 0]
    for m in measurements:
        if m.value <= 15:
            result[0] += m.value
        elif m.value <= 30:
            result[1] += m.value
        elif m.value <= 60:
            result[2] += m.value
        else:
            result[3] += m.value
    return result


def make_count_profile(measurements: list[Measurement]):
    result = [0, 0, 0, 0]
    for m in measurements:
        if m.value <= 15:
            result[0] += 1
        elif m.value <= 30:
            result[1] += 1
        elif m.value <= 60:
            result[2] += 1
        else:
            result[3] += 1
    return result


def merge_profiles(rc1: list[int], rc2: list[int]) -> list[int]:
    return [rc1[0] + rc2[0], rc1[1] + rc2[1], rc1[2] + rc2[2], rc1[3] + rc2[3]]


def render_quality_profile(profile: list[int]) -> Text:
    total = sum(profile)
    very_high = ceil(((profile[3] / total) * 100) / 2) if total > 0 else 0
    high = ceil(((profile[2] / total) * 100) / 2) if total > 0 else 0
    medium = ceil(((profile[1] / total) * 100) / 2) if total > 0 else 0
    low = 50 - very_high - high - medium
    parts = []
    if low > 0:
        parts.append(("|" * low, Style(color="green")))
    if medium > 0:
        parts.append(("|" * medium, Style(color="yellow")))
    if high > 0:
        parts.append(("|" * high, Style(color="dark_orange")))
    if very_high > 0:
        parts.append(("|" * very_high, Style(color="red")))
    return Text.assemble(*parts)


def path_has_extension(path: str, suffixes: Union[str, list[str]]):
    dot_index = path.rfind(".")
    if dot_index >= 0:
        suffix = path[dot_index + 1 :]
        if isinstance(suffixes, list):
            return suffix in suffixes
        else:
            return suffix == suffixes
    else:
        return False


def get_parent_folder(path: str) -> str:
    parts = path.split(os.path.sep)
    if len(parts) == 1:
        return "."
    else:
        return os.path.sep.join(parts[0:-1])


def get_basename(path: str) -> str:
    parts = path.split(os.path.sep)
    return parts[-1]


def calculate_checksum(path: str) -> str:
    with open(path, "rb") as file:
        file_bytes = file.read()
        return hashlib.md5(file_bytes).hexdigest()


def delete_indices(iterable: list, indices: list[int]) -> list[Any]:
    return [b for i, b in enumerate(iterable) if i not in indices]


def clear_screen() -> None:
    def isatty(stream) -> bool:
        try:
            return stream.isatty()
        except Exception:
            return False

    if not isatty(sys.stdout):
        return
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        sys.stdout.write("\033[2J\033[1;1H")


def format_measurement(path: str, measurement: Measurement) -> Text:
    result = Text()
    result.append(path, style="bold")
    result.append(":", style=Style(color="cyan"))
    result.append(str(measurement.start.line))
    result.append(":", style=Style(color="cyan"))
    result.append(str(measurement.start.column))
    result.append(":", style=Style(color="cyan"))
    result.append(" ")
    result.append(str(measurement.value))
    result.append(" ")
    if measurement.value > 60:
        result.append("\u2716", style=Style(color="red"))
    elif measurement.value > 30:
        result.append("\u26A0", style=Style(color="dark_orange"))
    elif measurement.value > 15:
        result.append("\u2713", style=Style(color="yellow"))
    else:
        result.append("\u2713", style=Style(color="green"))
    result.append(" ")
    result.append(measurement.unit_name)
    return result


def format_unit(name: str, length: int, file: Union[str, None] = None) -> Text:
    if length > 60:
        color = "red"
    elif length > 30:
        color = "dark_orange"
    elif length > 15:
        color = "yellow"
    else:
        color = "green"
    result = Text()
    result.append(f"{length:3}" if length < 1000 else str(length))
    result.append(Text(" | ", style=Style(color=color)))
    if file:
        result.append(Text(f"{file}:", style=Style(dim=True)))
    result.append(name)
    return result


def load_language_by_name(name: str) -> Language | None:
    name = name.replace("+", "p")
    try:
        module = importlib.import_module(f"codelimit.languages.{name}")
        language_class = getattr(module, f"{name}")
        return language_class()
    except ModuleNotFoundError:
        return None


def replace_string_literal_with_predicate(expression: Expression) -> Expression:
    if isinstance(expression, list):
        return [
            (
                TokenValue(item)
                if isinstance(item, str)
                else (
                    replace_string_literal_with_predicate(item)
                    if isinstance(item, Operator)
                    else item
                )
            )
            for item in expression
        ]
    else:
        return [
            (
                TokenValue(expression)
                if isinstance(expression, str)
                else (
                    replace_string_literal_with_predicate(expression)
                    if isinstance(expression, Operator)
                    else expression
                )
            )
        ]
