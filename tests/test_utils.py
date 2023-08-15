from codelimit.common.utils import format_unit


def test_format_unit():
    assert format_unit("bar()", 1).markup == "[[green]  1[/green]] bar()"
    assert format_unit("bar()", 20).markup == "[[yellow] 20[/yellow]] bar()"
    assert format_unit("bar()", 70).markup == "[[red]60+[/red]] bar()"
