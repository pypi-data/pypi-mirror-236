#!/usr/bin/env python
from typing import Annotated, Optional

import typer

from sshgen import __app_name__, __version__
from sshgen.logger import init_logger
from sshgen.models.loglevel import LogLevel
from sshgen.utils.app import AppUtils
from sshgen.utils.file import FileUtils

app = typer.Typer(no_args_is_help=True)


@app.command('generate')
def generate_hosts_file(hosts_file: Annotated[str, typer.Option('--hosts-file', '-h')] = './hosts.yml',
                        output: Annotated[str, typer.Option('--output', '-o')] = './config') -> None:
    """
    Command to generate SSH configuration file.
    By default, it uses file hosts.yml placed in your working directory and outputs to the file named "config"

    Example usage: sshconf generate -o my_ssh_config
    """

    hosts_file = FileUtils.as_file(file_path=hosts_file)
    output_file = FileUtils.as_file(file_path=output)

    AppUtils(hosts_file, output_file).generate_ssh_config()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} v{__version__}')
        raise typer.Exit()


# noinspection PyUnusedLocal
@app.callback()
def main(
        verbose: Annotated[
            Optional[bool],
            typer.Option('--verbose', is_eager=True, help='Switch log level to DEBUG, default is INFO.'),
        ] = False,
        version: Annotated[
            Optional[bool],
            typer.Option('-v', '--version', callback=_version_callback, is_eager=True),
        ] = None,
) -> None:
    """
    sshgen generates SSH configuration file based on an Ansible hosts file.
    """
    if verbose:
        init_logger(level=LogLevel.DEBUG)
    else:
        init_logger(level=LogLevel.INFO)


if __name__ == '__main__':
    app()
