from codelimit.common.Language import Language
from codelimit.languages.C import C
from codelimit.languages.CSharp import CSharp
from codelimit.languages.Cpp import Cpp
from codelimit.languages.Java import Java
from codelimit.languages.JavaScript import JavaScript
from codelimit.languages.Python import Python
from codelimit.languages.TypeScript import TypeScript


class Languages:
    by_name: dict[str, Language] = {}
    for subclass in Language.__subclasses__():
        language = subclass()
        by_name[language.name] = language
