from codelimit.languages import Languages
from tests.conftest import assert_functions


def test_simple_main_function():
    code = """
        fn main() {
            println!("Hello world!");
        }
    """

    assert_functions(code, Languages.Rust, {"main": 3})


def test_function_modifiers():
    code = """
        pub async fn foo() {
            bar().await;
        }

        pub(crate) const fn bar() -> u32 {
            42
        }
    """

    assert_functions(code, Languages.Rust, {"foo": 3, "bar": 3})


def test_generics_return_type_and_where_clause():
    code = """
        fn largest<'a, T>(items: &'a [T]) -> Option<&'a T>
        where
            T: PartialOrd,
        {
            items.iter().max_by(|a, b| a.partial_cmp(b).unwrap())
        }
    """

    assert_functions(code, Languages.Rust, {"largest": 6})


def test_impl_methods():
    code = """
        struct Foo {
            x: i32,
        }

        impl Foo {
            pub fn new(x: i32) -> Self {
                Foo { x }
            }

            fn get(&self) -> i32 {
                self.x
            }
        }

        impl Display for Foo {
            fn fmt(&self, f: &mut Formatter) -> fmt::Result {
                write!(f, "{}", self.x)
            }
        }
    """

    assert_functions(code, Languages.Rust, {"new": 3, "get": 3, "fmt": 3})


def test_trait_declarations_are_ignored():
    code = """
        trait Shape {
            fn area(&self) -> f64;

            fn describe(&self) -> String {
                format!("area: {}", self.area())
            }
        }
    """

    assert_functions(code, Languages.Rust, {"describe": 3})


def test_closure_is_not_a_function():
    code = """
        fn foo() {
            let add = |a, b| {
                a + b
            };
            add(1, 2);
        }
    """

    assert_functions(code, Languages.Rust, {"foo": 6})


def test_nested_functions():
    code = """
        fn outer() {
            fn inner() -> i32 {
                1
            }
            inner();
        }
    """

    assert_functions(code, Languages.Rust, {"outer": 3, "inner": 3})


def test_extern_block():
    code = """
        extern "C" {
            fn abs(input: i32) -> i32;
        }
    """

    assert_functions(code, Languages.Rust, {})


def test_skip_function_with_nocl_comment():
    code = """
        fn foo() {
            bar();
        }

        fn bar() { // nocl
            foo();
        }
    """

    assert_functions(code, Languages.Rust, {"foo": 3})


def test_nested_semi_colon_in_headers():
    code = """
        fn digest(input: [u8; 32]) {
            42;
        }
    """

    assert_functions(code, Languages.Rust, {"digest": 3})


def test_me():
    code = """
        fn map<U, F: FnOnce(T)>(self, f: F) -> Selection<U> {
            match self {
                Selection::Select(name, inner) => {
                    Selection::Select(name, f(inner))
                }
                Selection::Negate(name, inner) => {
                    Selection::Negate(name, f(inner))
                }
            }
        }
    """

    assert_functions(code, Languages.Rust, {"map": 10})
