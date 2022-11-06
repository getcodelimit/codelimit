from codelimit.common.Measurements import Measurements
from codelimit.common.Report import Report


def test_empty_measurements_collection():
    report = Report(Measurements())

    assert report.get_average() == 0
    assert report.ninetieth_percentile() == 0
    assert report.risk_categories() == [0, 0, 0, 0]
