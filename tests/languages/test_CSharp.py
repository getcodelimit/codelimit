from codelimit.languages import CSharp
from tests.conftest import assert_functions, print_scopes


def test_hello_world():
    code = """
    namespace SamplePrograms
    {
        public class HelloWorld
        {
            static void Main()
            {
                System.Console.WriteLine("Hello, World!");
            }
        }
    }
    """

    assert_functions(code, CSharp(), {"Main": 4})


def test_longest_word():
    code = """
    public class Foo {
        public void bar() {
            string[] w = sentence.Split(new[] {' '});
        }
    }
    """

    assert_functions(code, CSharp(), {"bar": 3})
