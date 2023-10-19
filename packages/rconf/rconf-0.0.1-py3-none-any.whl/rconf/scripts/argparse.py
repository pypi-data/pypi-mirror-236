"""argparse helper functions."""
from __future__ import annotations

import argparse
import shutil
import textwrap

try:
    # TODO: python-3.8
    from importlib.metadata import distribution
except ImportError:
    from importlib_metadata import distribution


class VersionAction(argparse.Action):
    """Version Action using importlib.metadata.distribution for a package name.

    It won't try to discover the package unless it's used.
    """

    def __init__(
        self,
        *args,
        package: str,
        help: str = "show program's version number and exit.",  # noqa: A002
        **kwargs,
    ) -> None:
        """Initialize VersionAction."""
        super().__init__(*args, nargs=0, help=help, **kwargs)
        self.package = package

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.ArgumentParser,  # noqa: ARG002
        values: list,  # noqa: ARG002
        option_string: str | None = None,  # noqa: ARG002
    ) -> None:
        """Print the package version."""
        parser.exit(
            status=0,
            message=f"{parser.prog} {distribution(self.package).version}\n",
        )


def add_commands_epilog(
    parser: argparse.ArgumentParser,
    commands: argparse._SubParsersAction,  # noqa: SLF001
) -> None:
    """Add epilog describing subcommands."""
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    width = shutil.get_terminal_size().columns - 2
    parser.epilog = "\n".join(
        f"{choice.prog}\n"
        + "\n".join(
            textwrap.wrap(
                choice.description,
                width,
                initial_indent="  ",
                subsequent_indent="  ",
            ),
        )
        for choice in commands.choices.values()
    )


def add_version(
    parser: argparse.ArgumentParser,
    package: str,
) -> VersionAction:
    """Add a version argument for a package."""
    return parser.add_argument("--version", action=VersionAction, package=package)
