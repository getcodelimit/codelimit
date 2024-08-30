from pathlib import Path
from typing import Annotated

import typer
from rich import print

from codelimit.commands.upload import upload_command
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


@app.command(help="Upload report to Code Limit GitHub App")
def upload(
    repository: Annotated[
        str, typer.Argument(show_default=False, help="GitHub repository")
    ],
    branch: Annotated[str, typer.Argument(show_default=False, help="GitHub branch")],
    report_file: Path = typer.Option(
        None,
        "--report",
        show_default=False,
        exists=True,
        dir_okay=False,
        file_okay=True,
        help="JSON report file",
    ),
    token: str = typer.Option(
        None, "--token", show_default=False, help="GitHub access token"
    ),
    url: str = typer.Option(
        "https://codelimit.vercel.app/api/upload",
        "--url",
        help="Upload JSON report to this URL.",
    ),
):
    upload_command(repository, branch, report_file, token, url)
