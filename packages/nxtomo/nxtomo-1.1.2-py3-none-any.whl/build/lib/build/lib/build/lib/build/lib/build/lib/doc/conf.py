# -- Project information -----------------------------------------------------

project = "nxtomo"
copyright = "2023, ESRF"
author = "P.Paleo, H.Payno, A. Mirone, J.Lesaint"

# The full version, including alpha/beta/rc tags
release = "1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.autosummary",
    "nbsphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "nature"

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

html_logo = "img/nxtomo.png"

# autosummary options
autosummary_generate = True

autodoc_default_flags = [
    "members",
    "undoc-members",
    "show-inheritance",
]
