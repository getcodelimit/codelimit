from enum import Enum


class LanguageName(Enum):
    C = "C"
    Cpp = "C++"
    Java = "Java"
    JavaScript = "JavaScript"
    Python = "Python"
    TypeScript = "TypeScript"


language_names = [entry.name for entry in LanguageName]
