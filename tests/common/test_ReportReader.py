from codelimit.common.Codebase import Codebase
from codelimit.common.SourceMeasurement import SourceMeasurement
from codelimit.common.report.Report import Report
from codelimit.common.report.ReportReader import ReportReader
from codelimit.common.report.ReportWriter import ReportWriter


def test_empty_report():
    codebase = Codebase()
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.uuid == report.uuid

    result_entries = result.codebase.tree['./'].entries
    result_measurements = result.codebase.measurements

    assert len(result_entries) == 0
    assert len(result_measurements) == 0


def test_single_file():
    codebase = Codebase()
    codebase.add_file('foo.py', [SourceMeasurement('bar()', 10, 20)])
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.uuid == report.uuid

    result_entries = result.codebase.tree['./'].entries
    result_measurements = result.codebase.measurements

    assert len(result_entries) == 1
    assert result_entries[0].is_file()
    assert result_entries[0].name == 'foo.py'
    assert len(result_measurements) == 1
    assert len(result_measurements['foo.py']) == 1
    assert result_measurements['foo.py'][0].start_line == 10
    assert result_measurements['foo.py'][0].value == 20


def test_multiple_files():
    codebase = Codebase()
    codebase.add_file('foo.py', [SourceMeasurement('spam()', 10, 20)])
    codebase.add_file('bar.py', [SourceMeasurement('eggs()', 10, 20), SourceMeasurement('ham()', 20, 30)])
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.uuid == report.uuid

    result_entries = result.codebase.tree['./'].entries
    result_measurements = result.codebase.measurements

    assert len(result_entries) == 2
    assert result_entries[0].is_file()
    assert result_entries[0].name == 'foo.py'
    assert result_entries[1].is_file()
    assert result_entries[1].name == 'bar.py'
    assert len(result_measurements) == 2
    assert len(result_measurements['foo.py']) == 1
    assert len(result_measurements['bar.py']) == 2
    assert result_measurements['bar.py'][1].start_line == 20
    assert result_measurements['bar.py'][1].value == 30


def test_multiple_files_and_folders():
    codebase = Codebase()
    codebase.add_file('foo.py', [SourceMeasurement('bar()', 10, 20)])
    codebase.add_file('bar/spam.py', [SourceMeasurement('spam()', 10, 20), SourceMeasurement('eggs()', 20, 30)])
    report = Report(codebase)

    json = ReportWriter(report).to_json()
    result = ReportReader.from_json(json)

    assert result.uuid == report.uuid

    result_entries = result.codebase.tree['./'].entries

    assert len(result_entries) == 2
    assert result_entries[0].is_file()
    assert result_entries[0].name == 'foo.py'
    assert result_entries[1].is_folder()
    assert result_entries[1].name == 'bar/'

    result_entries = result.codebase.tree['bar/'].entries

    assert len(result_entries) == 1
    assert result_entries[0].is_file()
    assert result_entries[0].name == 'spam.py'

    result_measurements = result.codebase.measurements

    assert len(result_measurements) == 2
    assert len(result_measurements['foo.py']) == 1
    assert len(result_measurements['bar/spam.py']) == 2
    assert result_measurements['bar/spam.py'][1].start_line == 20
    assert result_measurements['bar/spam.py'][1].value == 30
