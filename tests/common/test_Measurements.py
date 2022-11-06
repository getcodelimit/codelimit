from codelimit.common.Measurement import Measurement
from codelimit.common.Measurements import Measurements


def test_to_json():
    measurements = Measurements()
    m = Measurement('foo.py', 10, 10)
    measurements.add(m)

    assert measurements.to_json() == '[{"filename": "foo.py", "line": 10, "length": 10}]'


def test_to_json_multiple():
    measurements = Measurements()
    m = Measurement('foo.py', 10, 10)
    measurements.add(m)
    m = Measurement('bar.py', 20, 10)
    measurements.add(m)

    assert measurements.to_json() == '[{"filename": "foo.py", "line": 10, "length": 10}' + \
           ', {"filename": "bar.py", "line": 20, "length": 10}]'
