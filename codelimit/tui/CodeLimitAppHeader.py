import os.path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from codelimit.common.report.Report import Report
from codelimit.common.utils import get_basename
from codelimit.tui.QualityProfile import QualityProfile


class CodeLimitAppHeader(Widget):
    DEFAULT_CSS = """
    Vertical {
        background: #020409;
        border-bottom: solid #31363c;
        dock: top;
    }
    """

    def __init__(self, report: Report):
        super().__init__()
        self.report = report
        self.styles.height = 4

    def compose(self) -> ComposeResult:
        root = self.report.codebase.root
        title = Static(get_basename(root) + os.path.sep)
        title.styles.content_align_horizontal = "center"
        message = Static(self.report.summary())
        message.styles.content_align_horizontal = "center"
        yield Vertical(title, QualityProfile(self.report.quality_profile()), message)
