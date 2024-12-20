from pathlib import Path

from codelimit.common.GithubRepository import GithubRepository
from codelimit.common.ScanTotals import ScanTotals
from codelimit.common.report.ReportUnit import ReportUnit


def report_totals_markdown(st: ScanTotals) -> str:
    result = ""
    result += (
        "| **Language** | **Files** | **Lines of Code** | **Functions** | \u26A0 | \u274C |\n"
    )
    result += "| --- | ---: | ---: | ---: | ---: | ---: |\n"
    for lt in st.languages_totals():
        result += (
            f"| {lt.language} | "
            f"{lt.files} | "
            f"{lt.loc} | "
            f"{lt.functions} | "
            f"{lt.hard_to_maintain} | "
            f"{lt.unmaintainable} |\n"
        )
    if len(st.languages_totals()) > 1:
        result += (
            f"| **Totals** | "
            f"**{st.total_files()}** | "
            f"**{st.total_loc()}** | "
            f"**{st.total_functions()}** | "
            f"**{st.total_hard_to_maintain()}** | "
            f"**{st.total_unmaintainable()}** |"
        )
    result += "\n"
    result += "Generated by [CodeLimit](https://getcodelimit.github.io)"
    return result


def report_functions_markdown(root: Path | None, report_units: list[ReportUnit],
                              repository: GithubRepository | None = None) -> str:
    result = ""
    if repository:
        result += report_functions_markdown_with_repository(root, report_units, repository)
    else:
        result += report_functions_markdown_without_repository(root, report_units)
    result += "\n"
    result += "Generated by [CodeLimit](https://getcodelimit.github.io)"
    return result


def report_functions_markdown_without_repository(
        root: Path | None, report_units: list[ReportUnit]
) -> str:
    result = ""
    result += "| **File** | **Line** | **Column** | **Length** | **Function** |\n"
    result += "| --- | ---: | ---: | ---: | --- |\n"
    for unit in report_units:
        file_path = unit.file if root is None else root.joinpath(unit.file)
        type = "\u274C" if unit.measurement.value > 60 else "\u26A0"
        result += (
            f"| {str(file_path)} | {unit.measurement.start.line} | {unit.measurement.start.column} | "
            f"{unit.measurement.value} | {type} {unit.measurement.unit_name} |\n"
        )
    return result


def report_functions_markdown_with_repository(root: Path | None, report_units: list[ReportUnit],
                                              repository: GithubRepository) -> str:
    result = ""
    result += "| **Function** | **Length** |\n"
    result += "| --- | ---: |\n"
    for unit in report_units:
        violation_type = "\u274C" if unit.measurement.value > 60 else "\u26A0"
        owner = repository.owner
        name = repository.name
        branch = repository.branch
        link = (f'https://github.com/{owner}/{name}/blob/{branch}/{unit.file}#L{unit.measurement.start.line}-L'
                f'{unit.measurement.end.line}')
        result += (
            f"| {violation_type} \[{unit.measurement.unit_name}]({link}) | {unit.measurement.value} |\n"
        )
    return result
