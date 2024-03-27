from codelimit.languages import LanguageName
from tests.conftest import assert_units


def test_simple_main_function():
    code = """
    #include <iostream>

    using namespace std;
    
    int main(int argc, char *argv[]) {
        cout << "hello world!" << endl;
        return 0;
    }
    """

    assert_units(code, LanguageName.Cpp, {"main": 4})


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

    assert_units(code, LanguageName.Cpp, {"sayHello": 3, "main": 5})


def test_function():
    code = """
    ObjectContour
    makeInscribedOctagon(cv::Point2f circleCenter, float circleRadius, cv::Size imageSize) {
        if (circleCenter.x - circleRadius < 0.0f) {
            circleRadius = circleCenter.x;
        }
    }
    """

    assert_units(code, LanguageName.Cpp, {"makeInscribedOctagon": 5})


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

    assert_units(code, LanguageName.Cpp, {"sayHello": 3})
