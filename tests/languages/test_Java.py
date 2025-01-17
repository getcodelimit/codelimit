from codelimit.languages import Languages
from tests.conftest import assert_functions


def test_simple_main_function():
    code = """
        public class T {
            public static void main(String[] args) {
                System.out.println("Hello world!");
            }
        }
    """

    assert_functions(code, Languages.Java, {"main": 3})


def test_function_with_throws():
    code = """
        public class T {
            private void foo() throws Exception {
                throw new Exception();
            }
        }
    """

    assert_functions(code, Languages.Java, {"foo": 3})


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

    assert_functions(code, Languages.Java, {"one": 3, "two": 3})


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

    assert_functions(code, Languages.Java, {"Foo": 3, "foobar": 3})


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

    assert_functions(code, Languages.Java, {"Foo": 6, "preVisitDirectory": 6})


def test_record_class():
    code = """
    public record Person(String name, int age) {
        public Person {
            if (age < 0) {
                throw new IllegalArgumentException("Age must be non-negative");
            }
        }
        
        public static void main(String[] args) {
            Person p = new Person("Alice", 30);
            System.out.println(p);
        }
    }
    """

    assert_functions(code, Languages.Java, {"main": 4})


def test_method_with_anonymous_class():
    code = """
    class Foo {
        private void foo() {
            return new Bar() {
            };
        }
    }
    """

    assert_functions(code, Languages.Java, {"foo": 4})


def test_abstract_methods():
    code = """
    public abstract class Foo {
        abstract void foo();
        abstract void bar();
        
        public void foobar() {
            System.out.println("baz");
        }
    }
    """

    assert_functions(code, Languages.Java, {'foobar': 3})


def test_abstract_methods_with_inner_class():
    code = """
    public abstract class Foo {
        abstract void foo() throws Exception;

        class Bar {
            public void foobar() {
                System.out.println("baz");
            }
        }
    }
    """

    assert_functions(code, Languages.Java, {'foobar': 3})
