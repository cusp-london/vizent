import os
import sys
sys.path.insert(0, os.path.abspath('../vizent/'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'vizent'
copyright = '2023, CUSP London, Lucy McLaughlin'
author = 'CUSP London, Lucy McLaughlin'
release = '1.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['mpl_sphinx_theme', 'sphinx.ext.autodoc', 'nbsphinx']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme_options = {
    # logo is installed by mpl-sphinx-theme as:
    "logo": {"link": "",
            "image_light": "_static/vizent_logo_thumbnail.png",
            "image_dark": "_static/vizent_logo_thumbnail.png"},
    # if this default is OK, then no need to modify "logo"
    # collapse_navigation in pydata-sphinx-theme is slow, so skipped for local
    # and CI builds https://github.com/pydata/pydata-sphinx-theme/pull/386
    #"collapse_navigation": not is_release_build,
    "show_prev_next": False,
    # Determines the type of links produced in the navigation header:
    # - absolute: Links point to the URL https://matplotlib.org/...
    # - server-stable: Links point to top-level of the server /stable/...
    # - internal: Links point to the internal files as expanded by the `pathto`
    #   template function in Sphinx.
    "navbar_links": "absolute",
    # Theme options are theme-specific and customize the look and feel of a theme
    # further.  For a list of options available for each theme, see the
    # documentation.
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/cusp-london/vizent",
            "icon": "fab fa-github-square fa-xl",
        },
        {
            "name": "Twitter",
            "url": "https://twitter.com/cusplondon",
            "icon": "fab fa-twitter-square fa-xl",
        },
    ]
}


pypi='https://github.com/cusp-london/vizent/actions/workflows/unit-tests-minimal.yml/badge.svg'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'mpl_sphinx_theme'
html_static_path = ['_static']

# autodoc_type_aliases = {
#     'ArrayLike': 'ArrayLike', 
# }
autodoc_typehints='none'
#autodoc_typehints_format = 'short'
#python_use_unqualified_type_names = True