import json

import rconf

config = rconf.loadu("https://github.com/manifest.json#/icons/0/src")

# or explicitly
config_explicit = rconf.loadu(
    "https://github.com/manifest.json",
    ptr="/icons/0/src",
    media_type=".json",
)

print(json.dumps(config, indent=4))

assert config == config_explicit
