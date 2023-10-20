"""RConf CLI tool."""
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations

import argparse
import pathlib
import sys

import rconf

from . import config, dump
from .argparse import add_commands_epilog, add_version

arg_parser = argparse.ArgumentParser("rconf", description="RConf CLI tool")

arg_parser.add_argument(
    "-c",
    "--config-file",
    metavar="LOCATION",
    help="""location of a configuration file.
    Replaces other active configuration file, if any.""",
    type=pathlib.Path,
    default=None,
)

add_version(arg_parser, "rconf")

commands = arg_parser.add_subparsers(title="commands", required=True)
for command in [config, dump]:
    command_name = command.__name__.rsplit(".", maxsplit=1)[-1]
    subcommand = commands.add_parser(
        command_name,
        description=command.main.__doc__,
    )
    command.prepare_parser(subcommand)
    subcommand.set_defaults(command=command.main, command_name=command_name)

# TODO: python-3.11
if sys.version_info < (3, 11):
    commands.metavar = "{" + ",".join(commands.choices) + "}"

add_commands_epilog(arg_parser, commands)


def main() -> None:
    """RConf CLI tool."""
    try:
        from argcomplete import autocomplete

        autocomplete(arg_parser)
    except ModuleNotFoundError:
        pass
    args = arg_parser.parse_args()

    config_path = config.get_active(args)
    options: dict[str, rconf.Value] = {}
    if config_path is not None:
        options = rconf.loadu(config_path).get(args.command_name, {})

    args.command(args, **options)


if __name__ == "__main__":
    main()
