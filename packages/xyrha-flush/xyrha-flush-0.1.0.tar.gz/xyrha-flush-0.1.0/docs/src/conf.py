#!/usr/bin/env python3

"""This module contains the Sphinx configuration."""

from importlib.metadata import version as get_version

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "xyrha-flush"
copyright = "2023, DS422"
author = "DS422"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named "sphinx.ext.*") or your custom ones.
custom_extensions: list[str] = []

# DO NOT ADD ANY EXTENSIONS TO THIS LIST, USE THE `custom_extensions` list for your extensions
template_extensions: list[str] = ["sphinx.ext.viewcode", "sphinx.ext.doctest", "sphinx.ext.napoleon", "myst_parser"]

extensions = template_extensions + custom_extensions

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list[str] = []

source_suffix = [".rst", ".md"]

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
release = get_version("xyrha-flush")
# The short X.Y version.
version = ".".join(release.split(".")[:2])


myst_enable_extensions = ["colon_fence"]

add_module_names = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_material"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Output file base name for HTML help builder.
htmlhelp_basename = "xyrha_flush_doc"


html_theme_options = {
    "nav_title": "xyrha-flush",
    "color_primary": "blue",
    "color_accent": "light-blue",
    "globaltoc_depth": 2,
    "globaltoc_collapse": False,
    "globaltoc_includehidden": False,
    "version_dropdown": False,
    "master_doc": False,
}

html_sidebars = {"**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]}

html_show_sphinx = False
