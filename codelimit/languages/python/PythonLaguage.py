from codelimit.languages.Language import Language
from codelimit.languages.ScopeExtractor import ScopeExtractor
from codelimit.languages.python.PythonScopeExtractor import PythonScopeExtractor


class PythonLanguage(Language):

    def accept_file(self, path: str) -> bool:
        return path.lower().endswith('.py')

    def get_scope_extractor(self) -> ScopeExtractor:
        return PythonScopeExtractor()


