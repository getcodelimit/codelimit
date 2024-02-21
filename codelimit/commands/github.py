import typer
from rich import print

from codelimit.github_auth import device_flow_logout, device_flow_login

app = typer.Typer(no_args_is_help=True)


@app.command(help="Login to GitHub App")
def login():
    if device_flow_login():
        print("[green]Logged in successfully[/green]")
        typer.Exit(code=0)
    else:
        print("[red]Login failed[/red]")
        typer.Exit(code=1)


@app.command(help="Logout from GitHub App")
def logout():
    device_flow_logout()
    print("Logged out")
