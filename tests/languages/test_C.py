from codelimit.languages import Languages
from tests.conftest import assert_functions


def test_simple_main_function():
    code = """
        int main(int argc, char *argv) {
            return 0;
        }
    """

    assert_functions(code, Languages.C, {"main": 3})


def test_main_function_with_include():
    code = """
        #include <stdio.h>
        int main(int argc, char *argv[]) {
            printf("Hello world!");
            return 0;
        }
    """

    assert_functions(code, Languages.C, {"main": 4})


def test_simple_function():
    code = """
        #include <stdio.h>
        char * bar() {
            return "Hello world";
        }
    """

    assert_functions(code, Languages.C, {"bar": 3})


def test_multiple_functions():
    code = """
        #include <stdio.h>
        char * bar() {
            return "Hello world";
        }
        void foo() {
            printf(bar());
        }
    """

    assert_functions(code, Languages.C, {"bar": 3, "foo": 3})


def test_no_functions():
    code = ""

    assert_functions(code, Languages.C, {})


def test_iteration_macro_is_not_a_function():
    code = """
        void foo() {
            for_each_entry(entry) {
                remove_entry(entry);
            }
        }
    """

    assert_functions(code, Languages.C, {"foo": 5})


def test_formatting():
    code = """
        int nfs_register_sysctl(void)
        {
            nfs_callback_sysctl_table = register_sysctl_table(nfs_cb_sysctl_root);
            if (nfs_callback_sysctl_table == NULL)
                return -ENOMEM;
            return 0;
        }
    """

    assert_functions(code, Languages.C, {"nfs_register_sysctl": 7})


def test_nested_header_but_no_body_inside_parent():
    code = """
        void foo() {
            hlist_for_each_entry_safe(entry, n, &bucket->hlist, hnode) {
                kref_put(&entry->ref, nfs4_xattr_free_entry_cb);
            }
        }
        static struct bar = {
        };
    """

    assert_functions(code, Languages.C, {"foo": 5})
