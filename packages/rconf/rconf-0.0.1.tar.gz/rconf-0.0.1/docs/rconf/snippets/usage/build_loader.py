import json

import ppr_handler

import rconf

loader = rconf.build_loader(
    rconf.decode.INIHandler(("text/ini", ".ini")),
    ppr_handler.PprHandler(),
)
rconf.install_loader(loader)

doc = """
[DEFAULT]
some = one

[output_media_type]
$ref = ppr://rconf/scripts/rconf.toml#dump
"""

config = rconf.loads(doc, media_type=".ini")
print(json.dumps(config, indent=4))
