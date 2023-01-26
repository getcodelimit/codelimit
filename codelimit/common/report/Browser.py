import sys

from InquirerPy import inquirer, get_style
from InquirerPy.base import Choice

from codelimit.common.SourceFolderEntry import SourceFolderEntry
from codelimit.common.report.Report import Report
from codelimit.common.utils import clear_screen, header, register_shortcut


def _build_long_instruction():
    return u'[enter]:Select, [q]uit, [r]efactor list'


def _register_shortcuts(prompt):
    register_shortcut(prompt, 'q', 'quit')
    register_shortcut(prompt, 'r', 'refactor')


class Browser:
    def __init__(self, report: Report):
        self.report = report

    def show(self):
        path_parts = []
        while True:
            if len(path_parts) == 0:
                path = './'
            else:
                path = ''.join(path_parts)
            units = [Choice(value=entry, name=entry.name) for entry in
                     self.report.codebase.tree[path].entries if entry.is_folder()]
            clear_screen()
            header(self.report.risk_category_plot())
            prompt = inquirer.select(message='Select item', choices=units,
                                     long_instruction=_build_long_instruction(),
                                     style=get_style({'long_instruction': 'fg:#ffffff bg:#00008b'}, False))
            _register_shortcuts(prompt)
            choice = prompt.execute()
            command = 'select' if isinstance(choice, SourceFolderEntry) else choice['command']
            if command == 'quit':
                sys.exit()
            elif command == 'refactor':
                break
            elif command == 'select':
                path_parts.append(choice.name)
