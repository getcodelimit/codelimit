from math import ceil

from rich.console import RenderableType
from rich.style import Style
from rich.text import Text
from textual.widgets import Static


class QualityProfile(Static):
    def __init__(self, profile: list[int]):
        super().__init__()
        self.styles.content_align_horizontal = "center"
        self.profile = profile

    def render(self) -> RenderableType:
        total = sum(self.profile)
        very_high = ceil(((self.profile[3] / total) * 100) / 2) if total > 0 else 0
        high = ceil(((self.profile[2] / total) * 100) / 2) if total > 0 else 0
        medium = ceil(((self.profile[1] / total) * 100) / 2) if total > 0 else 0
        low = 50 - very_high - high - medium
        parts = []
        if low > 0:
            parts.append((" " * low, Style(bgcolor="green")))
        if medium > 0:
            parts.append((" " * medium, Style(bgcolor="yellow")))
        if high > 0:
            parts.append((" " * high, Style(bgcolor="dark_orange")))
        if very_high > 0:
            parts.append((" " * very_high, Style(bgcolor="red")))
        return Text.assemble(*parts)
