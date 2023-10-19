import json

import rconf

doc = """
{
"$ref": "https://github.com/manifest.json#/icons/0",
"/name": "GitHub icon"
}
"""

config = rconf.loads(doc)
print(json.dumps(config, indent=4))
