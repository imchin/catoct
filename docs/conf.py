import datetime
import string



# Package information
project = "CATOCT"
author = "Pi Thanacha Choopojcharoen"
copyright = f"2022-{datetime.date.today().year}, {author}"
release = version = pymanopt.__version__


# Build settings
extensions = [
    "myst_parser",
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxcontrib.katex",
]
master_doc = "index"
language = None

# Output options
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_style = "css/style.css"
#html_logo = "logo.png"
html_show_sphinx = False
html_baseurl = "catoct.org"
htmlhelp_basename = "catoctdoc"
html_last_updated_fmt = ""

# Doc version sidebar
templates_path = ["_templates"]

# autodoc
autodoc_typehints = "description"
autodoc_typehints_description_target = "all"
autodoc_default_options = {
    "member-order": "bysource",
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "inherited-members": True,
}

# nbsphinx
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]
nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base=None) %}
.. only:: html

    .. role:: raw-html(raw)
        :format: html
    .. nbinfo::
        :raw-html:`<a href="https://github.com/pymanopt/pymanopt/blob/master/{{
        docname }}"><img alt="Open on GitHub"
        src="https://img.shields.io/badge/Open-on%20GitHub-blue?logo=GitHub"
        style="vertical-align:text-bottom"></a>`
"""

