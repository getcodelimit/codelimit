from codelimit.common.utils import format_unit


def test_format_unit():
    assert format_unit("bar()", 1).markup == "  1[green] | [/green]bar()"
    assert format_unit("bar()", 20).markup == " 20[yellow] | [/yellow]bar()"
    assert format_unit("bar()", 70).markup == "60+[red] | [/red]bar()"
