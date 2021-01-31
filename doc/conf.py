# -*- coding: utf-8 -*-

import sys, re
from os.path import abspath
from pathlib import Path
from json import dump, loads

sys.path.insert(0, abspath('.'))

# -- General configuration ------------------------------------------------

needs_sphinx = '1.5'

extensions = [
    # Standard Sphinx extensions
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.graphviz',
    'sphinx.ext.viewcode',
]

autodoc_default_options = {
    "members": True,
    "private-members": True,
    "undoc-members": True,
}

templates_path = ['_templates']

source_suffix = {
    '.rst': 'restructuredtext',
}

master_doc = 'index'

project = u'Open Source Verification Bundle'
copyright = u'2021, Unai Martinez-Corral and contributors'
author = u'Unai Martinez-Corral and contributors'

version = "latest"
release = version  # The full version, including alpha/beta/rc tags.

language = None

exclude_patterns = []

# reST settings
prologPath = "prolog.inc"
try:
    with open(prologPath, "r") as prologFile:
        rst_prolog = prologFile.read()
except Exception as ex:
    print("[ERROR:] While reading '{0!s}'.".format(prologPath))
    print(ex)
    rst_prolog = ""

# -- Options for HTML output ----------------------------------------------

html_theme_options = {
    'logo_only': True,
    'home_breadcrumbs': False,
    'vcs_pageview_mode': 'blob',
}

html_context = {}
ctx = Path(__file__).resolve().parent / 'context.json'
if ctx.is_file():
    html_context.update(loads(ctx.open('r').read()))

html_theme_path = ["."]
html_theme = "_theme"

html_static_path = ['_static']

html_logo = str(Path(html_static_path[0]) / "logow.svg")
html_favicon = str(Path(html_static_path[0]) / "osvb.ico")

htmlhelp_basename = 'OSVBDoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
}

latex_documents = [
    (master_doc, 'OSVBDoc.tex', u'Open Source Verification Bundle Documentation', author, 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'OSVB', u'Open Source Verification Bundle Documentation', [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
  (master_doc, 'OSVB', u'Open Source Verification Bundle Documentation', author, 'OSVB', 'HDL verification.', 'Miscellaneous'),
]

# -- Sphinx.Ext.InterSphinx -----------------------------------------------

intersphinx_mapping = {
   'python': ('https://docs.python.org/3/', None),
   'ghdl': ('https://ghdl.github.io/ghdl', None),
   'ghdl-cosim': ('https://ghdl.github.io/ghdl-cosim', None),
   'vunit': ('https://vunit.github.io', None),
   'matplotlib': ('https://matplotlib.org/', None)
}

# -- Sphinx.Ext.ExtLinks --------------------------------------------------
extlinks = {
   'wikipedia': ('https://en.wikipedia.org/wiki/%s', None),
   'ghsharp':   ('https://github.com/umarcor/osvb/issues/%s', 'ghdl#'),
   'ghissue':   ('https://github.com/umarcor/osvb/issues/%s', 'issue #'),
   'ghpull':    ('https://github.com/umarcor/osvb/pull/%s', 'pull request #'),
   'ghsrc':     ('https://github.com/umarcor/osvb/blob/master/%s', None),
}
