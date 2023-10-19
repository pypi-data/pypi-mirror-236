import json
from http.client import InvalidURL

import rconf

doc = """
pypa_build."$ref" = "https://raw.githubusercontent.com/pypa/build/main/pyproject.toml#project.description"
icon."$ref" = "https://git INVALID hub.com/manifest.json#/icons/0"
"""

# No issues
config = rconf.loads(doc, ptr="pypa_build", media_type="toml")
print(json.dumps(config, indent=4))

# Raises InvalidURL
try:
    config = rconf.loads(doc, media_type="toml")
    rconf.TOMLPointer.parse("pypa_build").resolve(config)
except InvalidURL as error:
    print("As expected:", type(error), error)
