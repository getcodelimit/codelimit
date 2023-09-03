from codelimit.common.utils import format_unit


def test_format_unit():
    assert format_unit("bar()", 1).markup == "  1[green] | [/green]bar()"
    assert format_unit("bar()", 20).markup == " 20[yellow] | [/yellow]bar()"
    assert format_unit("bar()", 70).markup == " 70[red] | [/red]bar()"
    assert format_unit("bar()", 700).markup == "700[red] | [/red]bar()"
    assert format_unit("bar()", 7000).markup == "7000[red] | [/red]bar()"
