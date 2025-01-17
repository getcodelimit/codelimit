from codelimit.languages import Languages
from tests.conftest import assert_functions


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

    assert_functions(code, Languages.CSharp, {"Main": 4})


def test_longest_word():
    code = """
    public class Foo {
        public void bar() {
            string[] w = sentence.Split(new[] {' '});
        }
    }
    """

    assert_functions(code, Languages.CSharp, {"bar": 3})
