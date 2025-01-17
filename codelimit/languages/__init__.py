from codelimit.common.Language import Language
from codelimit.languages.C import C
from codelimit.languages.CSharp import CSharp
from codelimit.languages.Cpp import Cpp
from codelimit.languages.Java import Java
from codelimit.languages.JavaScript import JavaScript
from codelimit.languages.Python import Python
from codelimit.languages.TypeScript import TypeScript


class Languages:
    C = C()
    Cpp = Cpp()
    CSharp = CSharp()
    Java = Java()
    JavaScript = JavaScript()
    Python = Python()
    TypeScript = TypeScript()

    by_name: dict[str, Language] = {}
    for subclass in Language.__subclasses__():
        language = subclass() # type: ignore
        by_name[language.name] = language

