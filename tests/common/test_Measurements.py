from codelimit.common.Codebase import Codebase
from codelimit.common.SourceFile import SourceFile
from codelimit.common.SourceMeasurement import SourceMeasurement


def test_to_json():
    measurements = Codebase()
    file = SourceFile('foo.py', [SourceMeasurement(10, 10)])
    measurements.add(file)

    assert measurements.to_json() == '[{"path": "foo.py", "measurements": [{"start_line": 10, "value": 10}]}]'


def test_to_json_multiple():
    measurements = Codebase()
    file = SourceFile('foo.py', [SourceMeasurement(10, 10)])
    measurements.add(file)
    file = SourceFile('bar.py', [SourceMeasurement(20, 10)])
    measurements.add(file)

    assert measurements.to_json() == '[{"path": "foo.py", "measurements": [{"start_line": 10, "value": 10}]}' + \
           ', {"path": "bar.py", "measurements": [{"start_line": 20, "value": 10}]}]'


def test_all():
    measurements = Codebase()
    file = SourceFile('foo.py', [SourceMeasurement(10, 10)])
    measurements.add(file)
    file = SourceFile('bar.py', [SourceMeasurement(20, 10), SourceMeasurement(30, 10)])
    measurements.add(file)

    assert len(measurements.all_measurements()) == 3
