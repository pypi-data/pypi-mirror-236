"""Verify patches-result.toml matches patches.toml."""

import pathlib

import rconf

config = rconf.loadu(pathlib.Path(__file__).parent / "patches.toml")
assert config["rfc6902_patched"] == config["shorthand_patched"]
assert config["rfc6902_patched"] == rconf.loadu(
    pathlib.Path(__file__).parent / "patches-result.toml",
    ptr="rfc6902_patched",
)
