import os.path
from pathlib import Path

import click
from InquirerPy import inquirer, get_style
from InquirerPy.base import Choice

from codelimit.common.report.Browser import Browser
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportUnit import format_report_unit
from codelimit.common.source_utils import get_location_range
from codelimit.common.utils import clear_screen, register_shortcut, header


def _build_long_instruction():
    return "[enter]:Select, [q]uit, [b]rowse"


def _register_shortcuts(prompt):
    register_shortcut(prompt, "q", "quit")
    register_shortcut(prompt, "b", "browse")


class RefactorList:
    def __init__(self, report: Report, path: Path = "."):
        self.report = report
        self.path = path

    def show(self):
        units = [
            Choice(value=unit, name=format_report_unit(unit))
            for unit in self.report.all_report_units_sorted_by_length_asc()
        ]
        while True:
            clear_screen()
            header(self.report.risk_category_plot())
            prompt = inquirer.select(
                message="Select unit",
                choices=units,
                long_instruction=_build_long_instruction(),
                style=get_style({"long_instruction": "fg:#ffffff bg:#00008b"}, False),
            )
            _register_shortcuts(prompt)
            choice = prompt.execute()
            command = choice["command"] if "command" in choice else "select"
            if command == "quit":
                break
            elif command == "browse":
                Browser(self.report).show()
            elif command == "select":
                self.show_snippet(choice)

    def show_snippet(self, choice: dict):
        file_path = os.path.join(self.path, choice["file"])
        with open(file_path) as file:
            code = file.read()
        snippet = get_location_range(
            code, choice["measurement"]["start"], choice["measurement"]["end"]
        )
        click.echo(snippet)
        inquirer.text(
            "[Press ENTER to continue]", raise_keyboard_interrupt=False
        ).execute()
