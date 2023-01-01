from codelimit.common.Codebase import Codebase
from codelimit.common.Report import Report
from codelimit.common.ReportSerializer import ReportSerializer


def test_empty_measurements_collection():
    report = Report(Codebase())

    assert report.get_average() == 0
    assert report.ninetieth_percentile() == 0
    assert report.risk_categories() == [0, 0, 0, 0]

    serializer = ReportSerializer(report)

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
    json += '    "measurements": {\n'
    json += '    }\n'
    json += '  }\n'
    json += '}\n'

    assert serializer.to_json() == json
