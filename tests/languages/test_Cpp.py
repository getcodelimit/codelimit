from codelimit.languages import Languages
from tests.conftest import assert_functions


def test_simple_main_function():
    code = """
    #include <iostream>

    using namespace std;
    
    int main(int argc, char *argv[]) {
        cout << "hello world!" << endl;
        return 0;
    }
    """

    assert_functions(code, Languages.Cpp, {"main": 4})


def test_simple_class_function():
    code = """
    #include <iostream>

    using namespace std;
    
    class Main {
        public:
            void sayHello() {
                cout << "hello world!" << endl;
            }
    };
    
    int main(int argc, char *argv[]) {
        Main main;
        main.sayHello();
        return 0;
    }
    """

    assert_functions(code, Languages.Cpp, {"sayHello": 3, "main": 5})


def test_function():
    code = """
    ObjectContour
    makeInscribedOctagon(cv::Point2f circleCenter, float circleRadius, cv::Size imageSize) {
        if (circleCenter.x - circleRadius < 0.0f) {
            circleRadius = circleCenter.x;
        }
    }
    """

    assert_functions(code, Languages.Cpp, {"makeInscribedOctagon": 5})


def test_namespace():
    code = """
    #include <iostream>

    using namespace std;
    
    namespace Test {
    
    class Main {
        public:
            void sayHello() {
                cout << "hello world!" << endl;
            }
    };
    
    }
    """

    assert_functions(code, Languages.Cpp, {"sayHello": 3})


def test_skip_function_with_nocl_comment():
    code = """
    void foo(Bar bar) {
        bar.foo();
    }
    """

    assert_functions(code, Languages.Cpp, {"foo": 3})

    code = """
    void foo(Bar bar) { // nocl
        bar.foo();
    }
    """

    assert_functions(code, Languages.Cpp, {})
