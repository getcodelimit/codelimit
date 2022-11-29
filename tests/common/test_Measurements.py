from codelimit.common.Codebase import Codebase
from codelimit.common.SourceMeasurement import SourceMeasurement


def test_to_json():
    codebase = Codebase()
    codebase.add_file('foo.py', [SourceMeasurement(10, 10)])

    assert codebase.to_json() == '{"tree": {".": {"entries": [{"name": "foo.py"}]}}, "measurements": ' + \
           '{"foo.py": [{"start_line": 10, "value": 10}]}}'


def test_to_json_multiple():
    codebase = Codebase()
    codebase.add_file('foo.py', [SourceMeasurement(10, 10)])
    codebase.add_file('bar.py', [SourceMeasurement(20, 10)])

    expected = '{"tree": {".": {"entries": [{"name": "foo.py"}, {"name": "bar.py"}]}}, ' + \
               '"measurements": {"foo.py": [{"start_line": 10, "value": 10}], "bar.py": ' + \
               '[{"start_line": 20, "value": 10}]}}'
    assert codebase.to_json() == expected


def test_all():
    measurements = Codebase()
    measurements.add_file('foo.py', [SourceMeasurement(10, 10)])
    measurements.add_file('bar.py', [SourceMeasurement(20, 10), SourceMeasurement(30, 10)])

    assert len(measurements.all_measurements()) == 3
