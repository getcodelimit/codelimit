from codelimit.common.SourceFile import SourceFile
from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.Codebase import Codebase


def test_to_json():
    measurements = Codebase()
    file = SourceFile('foo.py', [SourceMeasurement(10, 10)])
    measurements.add(file)

    assert measurements.to_json() == '[{"path": "foo.py", "measurements": [{"line": 10, "length": 10}]}]'


def test_to_json_multiple():
    measurements = Codebase()
    file = SourceFile('foo.py', [SourceMeasurement(10, 10)])
    measurements.add(file)
    file = SourceFile('bar.py', [SourceMeasurement(20, 10)])
    measurements.add(file)

    assert measurements.to_json() == '[{"path": "foo.py", "measurements": [{"line": 10, "length": 10}]}' + \
           ', {"path": "bar.py", "measurements": [{"line": 20, "length": 10}]}]'


def test_all():
    measurements = Codebase()
    file = SourceFile('foo.py', [SourceMeasurement(10, 10)])
    measurements.add(file)
    file = SourceFile('bar.py', [SourceMeasurement(20, 10), SourceMeasurement(30, 10)])
    measurements.add(file)

    assert len(measurements.all_measurements()) == 3
