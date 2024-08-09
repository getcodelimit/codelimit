from codelimit.languages import Languages
from tests.conftest import assert_units, print_units


def test_simple_main_function():
    code = """
        public class T {
            public static void main(String[] args) {
                System.out.println("Hello world!");
            }
        }
    """

    assert_units(code, Languages.Java, {"main": 3})


def test_function_with_throws():
    code = """
        public class T {
            private void foo() throws Exception {
                throw new Exception();
            }
        }
    """

    assert_units(code, Languages.Java, {"foo": 3})


def test_two_functions():
    code = """
        public class T {
            private int one() {
                return 1;
            }
            private int two() {
                return 2;
            }
        }
    """

    assert_units(code, Languages.Java, {"one": 3, "two": 3})


def test_nested_class():
    code = """
    class Foo {
        public Foo() {
            System.out.println("Hello world!");
        }
        static class Bar {
            String foobar() {
                return "foobar";
            }
        }
    }
    """

    assert_units(code, Languages.Java, {"Foo": 3, "foobar": 3})


def test_anonymous_class():
    code = """
    class Foo {
        private Foo() {
            Files.walkFileTree(dir, new SimpleFileVisitor<Path>() {
                public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) {
                    if (!dir.equals(CloseablePath.this.dir)) {
                        tryToResetPermissions(dir);
                    }
                    return CONTINUE;
                }
            });
            return this;
        }
    }
    """

    print_units(code, Languages.Java)
    assert_units(code, Languages.Java, {"Foo": 6, "preVisitDirectory": 6})
