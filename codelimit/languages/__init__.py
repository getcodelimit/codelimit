from codelimit.languages.C import C
from codelimit.languages.Cpp import Cpp
from codelimit.languages.Java import Java
from codelimit.languages.JavaScript import JavaScript
from codelimit.languages.Python import Python
from codelimit.languages.TypeScript import TypeScript


class Languages:
    C = C()
    Cpp = Cpp()
    Java = Java()
    JavaScript = JavaScript()
    Python = Python()
    TypeScript = TypeScript()

    by_name = {
        C.name: C,
        Cpp.name: Cpp,
        Java.name: Java,
        JavaScript.name: JavaScript,
        Python.name: Python,
        TypeScript.name: TypeScript,
    }
