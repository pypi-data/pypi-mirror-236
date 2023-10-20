"""Dump a JSON or TOML document or fragment with references and patches."""
from __future__ import annotations

import importlib
import json
import logging
import pathlib
import sys
import typing

import rconf

if typing.TYPE_CHECKING:
    import argparse


def prepare_parser(parser: argparse.ArgumentParser) -> None:
    """Populate the dump argument parser."""
    parser.add_argument(
        "url",
        help="""the file location or '-' (stdin).
        URLs may contain a pointer as fragment.
        Add a scheme if needed (file, http, https, ftp or data).""",
        type=str,
    )

    parser.add_argument(
        "-b",
        "--base-url",
        help="URL to resolve relative references from, or use as URL for stdin.",
        type=str,
    )

    parser.add_argument(
        "-m",
        "--media-type",
        help="explicitly set input media type or filename extension.",
        type=str,
    )

    parser.add_argument(
        "-p",
        "--ptr",
        help="""a pointer to a fragment of the document.
        Overrides the URL fragment.""",
        type=str,
    )

    parser.add_argument(
        "-M",
        "--output-media-type",
        help="explicitly set output media type.",
        type=str,
    )


DUMPERS = {
    "str": {"callable": str},
    "json": {"callable": json.dumps, "indent": 4},
}

LOADER = {}


def main(
    args: argparse.Namespace,
    base_url: str | None = None,
    media_type: str | None = None,
    output_media_type: str = "json",
    loader: dict[str, typing.Any] | None = LOADER,
    dumpers: dict[str, dict[str, typing.Any]] = {},  # noqa: B006
) -> None:
    """Dump a JSON or TOML document or fragment with references and patches."""
    logger = logging.getLogger(pathlib.Path(sys.argv[0]).name)

    dumpers = {**DUMPERS, **dumpers}

    # CLI options
    base_url = args.base_url or base_url
    media_type = args.media_type or media_type
    output_media_type = args.output_media_type or output_media_type

    # Loader
    # translate handlers
    handlers = []
    if "handlers" in loader:
        for handler in loader["handlers"]:
            pkg_name, cls_name = handler["class"].rsplit(".", 1)
            handler_cls = getattr(importlib.import_module(pkg_name), cls_name)
            del handler["class"]
            if "pointer_type" in handler:
                pkg_name, cls_name = handler["pointer_type"].rsplit(".", 1)
                handler["pointer_type"] = getattr(
                    importlib.import_module(pkg_name),
                    cls_name,
                )
            if "media_types" in handler:
                media_types = handler["media_types"]
                del handler["media_types"]
                handlers.append(handler_cls(*media_types, **handler))
            else:
                handlers.append(handler_cls(**handler))
        del loader["handlers"]
    loader = rconf.build_loader(*handlers, **loader)

    # Dumpers
    if output_media_type in dumpers:
        dumper_options = dumpers[output_media_type]
        if isinstance(dumper_options["callable"], str):
            pkg_name, dumper_name = dumper_options["callable"].rsplit(".", 1)
            dumper = getattr(importlib.import_module(pkg_name), dumper_name)
        else:
            dumper = dumper_options["callable"]
        del dumper_options["callable"]
    else:
        logger.error("Unknown output media type %s.", output_media_type)
        sys.exit(1)

    try:
        if args.url == "-":
            value = loader.loads(sys.stdin.read(), media_type, base_url, ptr=args.ptr)
        else:
            value = loader.loadu(args.url, media_type, base_url=base_url, ptr=args.ptr)
    except Exception as error:
        logger.exception("%s while loading.", type(error).__name__)
        sys.exit(1)

    try:
        print(dumper(value, **dumper_options))
    except Exception as error:
        logger.exception("%s while dumping.", type(error).__name__)
        sys.exit(1)
