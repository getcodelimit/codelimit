from codelimit.common.CodebseEntry import CodebaseEntry


class SourceFolderEntry(CodebaseEntry):
    def __init__(self, path: str):
        super().__init__(path)

    def is_folder(self):
        return True

    def is_file(self):
        return False
