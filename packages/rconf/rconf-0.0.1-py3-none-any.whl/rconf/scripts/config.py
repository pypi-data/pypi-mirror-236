"""Show configuration options."""
from __future__ import annotations

import os
import pathlib
import sys
import typing

from .argparse import add_commands_epilog

if typing.TYPE_CHECKING:
    import argparse


CONFIG_PATH = "rconf/rconf.toml"


def get_list(args: argparse.Namespace) -> list[pathlib.Path]:
    """Get the list of potential configuration file locations."""
    candidates: list[pathlib.Path] = []

    # arguments
    if args.config_file:
        candidates.append(args.config_file)

    # virtual environment
    virtualenv = os.environ.get("VIRTUALENV", "").strip()
    if virtualenv:
        candidates.append(pathlib.Path(virtualenv) / ("." + CONFIG_PATH))

    # user
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "").strip()
        if appdata:
            candidates.append(pathlib.Path(appdata) / CONFIG_PATH)
        localappdata = os.environ.get("LOCALAPPDATA", "").strip()
        if localappdata:
            candidates.append(pathlib.Path(localappdata) / CONFIG_PATH)
        candidates.append(pathlib.Path.home() / CONFIG_PATH)
    elif sys.platform == "darwin":
        # https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/MacOSXDirectories/MacOSXDirectories.html
        candidates.append(
            pathlib.Path.home() / "Library/Application Support" / CONFIG_PATH,
        )
        candidates.append(pathlib.Path.home() / ".config" / CONFIG_PATH)
    else:
        # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME", "").strip()
        if xdg_config_home:
            candidates.append(pathlib.Path(xdg_config_home) / CONFIG_PATH)
        candidates.append(pathlib.Path.home() / ".config" / CONFIG_PATH)

    return candidates


def get_active(args: argparse.Namespace) -> pathlib.Path | None:
    """Get the active configuration file."""
    for candidate in get_list(args):
        candidate = candidate.expanduser().resolve()  # noqa: PLW2901
        if candidate.is_file():
            return candidate
    return None


def print_list(args: argparse.Namespace) -> None:
    """Print the list of considered configuration files."""
    found = False
    for candidate in get_list(args):
        candidate = candidate.expanduser().resolve()  # noqa: PLW2901
        is_file = candidate.is_file()
        print(
            str(candidate),
            "(active)"
            if (not found and is_file)
            else "(present)"
            if is_file
            else "(not found)",
        )
        found = found or is_file


def print_active(args: argparse.Namespace) -> None:
    """Print the content of the active configuration file."""
    active = get_active(args)
    if active is None:
        print("# No active configuration found.")
    else:
        with active.open("r") as config_file:
            print(config_file.read())


def print_demo(
    _: argparse.Namespace,
    file: typing.TextIO = sys.stdout,
) -> None:
    """Print the content of a demo configuration file."""
    with (pathlib.Path(__file__).parent / "rconf.toml").open("r") as config_file:
        print(config_file.read(), file=file)


def create(args: argparse.Namespace) -> None:
    """Create a configuration file."""
    config_path = get_list(args)[0]
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if config_path.is_file():
        print(config_path, "already exists.")
        if input("Overwrite? [y/N] ").casefold() not in ("y", "yes"):
            return
    with pathlib.Path(config_path).open("w", encoding="utf-8") as file:
        print_demo(args, file)
    print("Created", config_path)


def prepare_parser(parser: argparse.ArgumentParser) -> None:
    """Populate the config argument parser."""
    commands = parser.add_subparsers(title="subcommands", required=True)
    for command in [print_list, print_active, print_demo, create]:
        command_name = command.__name__.rsplit("_", maxsplit=1)[-1]
        subcommand = commands.add_parser(
            command_name,
            description=command.__doc__,
        )
        subcommand.set_defaults(subcommand=command, subcommand_name=command_name)
    add_commands_epilog(parser, commands)


def main(args: argparse.Namespace) -> None:
    """Show configuration options."""
    args.subcommand(args)
