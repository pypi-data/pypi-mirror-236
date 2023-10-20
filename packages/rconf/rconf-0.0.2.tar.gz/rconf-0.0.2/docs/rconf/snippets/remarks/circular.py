import json

import rconf

doc = """
[table]
strings = ["Hello", "TOML"]
circular."$ref" = "#table"
"""

config = rconf.loads(doc, media_type="toml")
print(config)

try:
    print(json.dumps(config, indent=4))
except ValueError as error:
    print("As expected:", type(error), error)

assert config["table"] == config["table"]["circular"]
