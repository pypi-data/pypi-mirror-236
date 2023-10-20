"""Sphinx Configuration.

http://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# Sphinx configuration conventions vs python conventions
import datetime
import pathlib
import sys

try:
    # TODO: python-3.8
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

sys.path.insert(0, str(pathlib.Path("../../src/").resolve()))

# Project information
project = "RConf"
author = "Filip Thyssen"
copyright_statememt = (
    str(datetime.datetime.now(tz=datetime.timezone.utc).year) + ", " + author
)
copyright = copyright_statememt  # noqa: A001
release = version("rconf")
version = ".".join(release.split(".")[:3])

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.autoprogram",
    "sphinx_design",
]
source_suffix = [".rst"]

root_doc = "index"
exclude_patterns = ["build", "dist", ".git"]
numfig = True

# Extension configuration
autodoc_default_options = {
    "member-order": "bysource",
}
autodoc_type_aliases = {
    "Leaf": "rconf.Leaf",
    "Value": "rconf.Value",
    "Key": "rconf.Key",
    "Pointer": "rconf.pointer.Pointer",
    "Patch": "rconf.patch.Patch",
}
autodoc_class_signature = "separated"
autodoc_typehints = "description"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}

# Options for HTML output
html_theme = "pydata_sphinx_theme"

html_show_sphinx = True
html_show_sourcelink = False

html_static_path = ["static"]
html_css_files = ["custom.css"]

html_theme_options = {
    "github_url": "https://github.com/fthyssen/rconf",
    "navbar_align": "left",
    "show_nav_level": 2,
    "show_toc_level": 1,
    "footer_start": ["sphinx-version"],
}
