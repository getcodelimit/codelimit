from textual.widgets import ListView, ListItem, Label

from codelimit.common.report.Report import Report


class CodebaseBrowserListView(ListView):
    def __init__(self, report: Report):
        super().__init__()
        self.report = report
        self.current_folder = report.codebase.tree["./"]
        self.load_current_folder()

    def load_current_folder(self):
        self.clear()
        for idx, entry in enumerate(self.current_folder.entries):
            list_item = ListItem(Label(entry.name), name=str(idx))
            self.append(list_item)

    def on_list_view_selected(self, event: ListView.Selected):
        idx = int(event.item.name)
        entry = self.current_folder.entries[idx]
        if entry.is_folder():
            self.current_folder = self.report.codebase.tree[f"{entry.path}/"]
            self.load_current_folder()
        else:
            self.post_message(entry)
