from enum import Enum


class Language(Enum):
    C = "C"
    Cpp = "C++"
    Java = "Java"
    JavaScript = "JavaScript"
    Python = "Python"
    TypeScript = "TypeScript"


ignored = [
    "ASCII armored",
    "ASN.1",
    "Awk",
    "Bash",
    "Batchfile",
    "BC",
    "CMake",
    "CSS",
    "Diff",
    "Docker",
    "Graphviz",
    "HTML",
    "INI",
    "JSON",
    "Kconfig",
    "Makefile",
    "Markdown",
    "Nginx configuration file",
    "Protocol Buffer",
    "reStructuredText",
    "Text only",
    "TOML",
    "VimL",
    "XML",
    "YAML",
]
