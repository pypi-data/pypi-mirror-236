import rconf

doc = """
[table]
strings = ["Hello", "TOML"]

[table.circular]
"$ref" = "#table"
"strings.1" = "toml"
"""

try:
    rconf.loads(doc, media_type="toml")
except rconf.DecodeError as error:
    print("As expected:", type(error), error)
