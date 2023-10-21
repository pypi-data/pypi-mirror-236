from typing import List, Optional

import typer

from arraylake_client import __version__
from arraylake_client import config as config_obj
from arraylake_client.cli.auth import auth
from arraylake_client.cli.config import app as config_app
from arraylake_client.cli.repo import app as repo_app
from arraylake_client.cli.utils import rich_console
from arraylake_client.diagnostics import get_diagnostics

app = typer.Typer(no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]}, rich_markup_mode="markdown")


def version_callback(value: bool):
    if value:
        rich_console.print(f"arraylake, version {__version__}")
        raise typer.Exit()


def diagnostics_callback(value: bool):
    if value:
        service_uri = config_obj.get("service.uri", None)
        diagnostics = get_diagnostics(service_uri=service_uri)
        rich_console.print(diagnostics)
        raise typer.Exit()


@app.callback()
def main(
    config: Optional[List[str]] = typer.Option([], help="arraylake config key-value (`key=value`) pairs to pass to sub commands"),
    version: Optional[bool] = typer.Option(None, "--version", callback=version_callback, is_eager=True, help="print Arraylake version"),
    diagnostics: Optional[bool] = typer.Option(
        None, "--diagnostics", callback=diagnostics_callback, is_eager=True, help="print Arraylake system diagnostics"
    ),
):
    """Manage ArrayLake from the command line."""
    if config:
        opts = dict(map(lambda x: x.split("="), config))
        config_obj.set(opts, priority="new")


app.add_typer(auth, name="auth")
app.add_typer(repo_app, name="repo")
app.add_typer(config_app, name="config")
