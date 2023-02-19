from codelimit.common.Codebase import Codebase
from codelimit.common.Location import Location
from codelimit.common.Measurement import Measurement
from codelimit.common.SourceFileEntry import SourceFileEntry
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportWriter import ReportWriter


def test_empty_measurements_collection():
    report = Report(Codebase())

    assert report.get_average() == 0
    assert report.ninetieth_percentile() == 0
    assert report.quality_profile() == [0, 0, 0, 0]

    serializer = ReportWriter(report)

    json = ''
    json += '{\n'
    json += f'  "uuid": "{report.uuid}",\n'
    json += '  "codebase": {\n'
    json += '    "tree": {\n'
    json += '      "./": {\n'
    json += '        "entries": [\n'
    json += '        ],\n'
    json += '        "profile": [0, 0, 0, 0]\n'
    json += '      }\n'
    json += '    },\n'
    json += '    "files": {\n'
    json += '    }\n'
    json += '  }\n'
    json += '}\n'

    assert serializer.to_json() == json


def test_all_units():
    codebase = Codebase()
    codebase.add_file(SourceFileEntry('foo.py', 'abcd1234',
                                      [Measurement('bar()', Location(10, 1), Location(30, 1), 20)]))
    report = Report(codebase)

    assert len(report.all_report_units_sorted_by_length_asc()) == 1
