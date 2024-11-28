from codelimit.common.LanguageTotals import LanguageTotals
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.SourceFolder import SourceFolder
from codelimit.common.Measurement import Measurement
from codelimit.common.utils import get_parent_folder, get_basename, merge_profiles


class Codebase:
    def __init__(self, root: str):
        self.root = root
        self.tree = {"./": SourceFolder()}
        self.files: dict[str, SourceFileEntry] = {}
        self.totals: dict[str, LanguageTotals] = {}

    def add_file(self, entry: SourceFileEntry):
        self.files[entry.path] = entry
        if entry.language not in self.totals:
            self.totals[entry.language] = LanguageTotals(entry.language)
        self.totals[entry.language].add(entry)
        parent_folder = get_parent_folder(entry.path)
        if f"{parent_folder}/" not in self.tree:
            self.add_folder(parent_folder)
        folder = self.tree[f"{parent_folder}/"]
        folder.add_file(entry)

    def add_folder(self, path: str):
        if path == ".":
            return
        if f"{path}/" not in self.tree:
            self.tree[f"{path}/"] = SourceFolder()
            self.add_folder(get_parent_folder(path))
            parent_folder = self.tree[f"{get_parent_folder(path)}/"]
            parent_folder.add_folder(get_basename(path))

    def aggregate(self):
        def aggregate_folder(path):
            folder = self.tree[path]
            for entry in folder.entries:
                if entry.is_folder():
                    if path == "./":
                        sub_folder = entry.name
                    else:
                        sub_folder = f"{path}{entry.name}"
                    folder.profile = merge_profiles(
                        folder.profile, aggregate_folder(sub_folder)
                    )

                else:
                    folder.profile = merge_profiles(folder.profile, entry.profile())
            return folder.profile

        aggregate_folder("./")

    def all_files(self) -> list[str]:
        return list(self.files.keys())

    def all_measurements(self) -> list[Measurement]:
        result = []
        for entry in self.files.values():
            result.extend(entry.measurements())
        return result

    def all_measurements_sorted_by_length_asc(self):
        return sorted(self.all_measurements(), key=lambda m: m.value, reverse=True)

    def total_loc(self) -> int:
        result = 0
        for m in self.all_measurements():
            result += m.value
        return result
