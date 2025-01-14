from codelimit.common.Codebase import Codebase
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.report.Report import Report


def test_empty_measurements_collection():
    report = Report(Codebase("/"))

    assert report.get_average() == 0
    assert report.ninetieth_percentile() == 0
    assert report.quality_profile() == [0, 0, 0, 0]


def test_quality_profile_percentage():
    report = Report(Codebase("/"))
    assert report.quality_profile_percentage() == (100, 0, 0, 0)


def test_quality_profile_percentage_rounding():
    report = Report(Codebase("/"))
    report.quality_profile = lambda: [2530, 2883, 1395, 0]
    assert report.quality_profile_percentage() == (36, 43, 21, 0)

    report.quality_profile = lambda: [630, 300, 70, 0]
    assert report.quality_profile_percentage() == (63, 30, 7, 0)

def test_all_units():
    codebase = Codebase("/")
    codebase.add_file(
        SourceFileEntry(
            "foo.py",
            "abcd1234",
            "Python",
            20,
            [Measurement("bar()", Location(10, 1), Location(30, 1), 20)],
        )
    )
    report = Report(codebase)

    assert len(report.all_report_units_sorted_by_length_asc()) == 1
