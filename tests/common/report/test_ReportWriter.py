from codelimit.common.Codebase import Codebase
from codelimit.common.GithubRepository import GithubRepository
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportWriter import ReportWriter


def test_to_json():
    report = Report(Codebase("/"))

    writer = ReportWriter(report)

    json = ""
    json += "{\n"
    json += f'  "version": "{report.version}",\n'
    json += f'  "uuid": "{report.uuid}",\n'
    json += f'  "timestamp": "{report.timestamp}",\n'
    json += '  "root": "/",\n'
    json += '  "codebase": {\n'
    json += '    "totals": {\n'
    json += "    },\n"
    json += '    "tree": {\n'
    json += '      "./": {\n'
    json += '        "entries": [\n'
    json += "        ],\n"
    json += '        "profile": [0, 0, 0, 0]\n'
    json += "      }\n"
    json += "    },\n"
    json += '    "files": {\n'
    json += "    }\n"
    json += "  }\n"
    json += "}\n"

    assert writer.to_json() == json


def test_to_json_with_repository():
    repository = GithubRepository("getcodelimit", "codelimit", branch="main")
    report = Report(Codebase("/"), repository)

    writer = ReportWriter(report)

    json = ""
    json += "{\n"
    json += f'  "version": "{report.version}",\n'
    json += f'  "uuid": "{report.uuid}",\n'
    json += f'  "timestamp": "{report.timestamp}",\n'
    json += '  "root": "/",\n'
    json += '  "repository": {\n'
    json += '    "owner": "getcodelimit",\n'
    json += '    "name": "codelimit",\n'
    json += '    "branch": "main"\n'
    json += '  },\n'
    json += '  "codebase": {\n'
    json += '    "totals": {\n'
    json += "    },\n"
    json += '    "tree": {\n'
    json += '      "./": {\n'
    json += '        "entries": [\n'
    json += "        ],\n"
    json += '        "profile": [0, 0, 0, 0]\n'
    json += "      }\n"
    json += "    },\n"
    json += '    "files": {\n'
    json += "    }\n"
    json += "  }\n"
    json += "}\n"

    assert writer.to_json() == json
