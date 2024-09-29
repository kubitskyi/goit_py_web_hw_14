# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Define the project root path
project_root = Path('../..')

# Load environment variables from .env file
load_dotenv(dotenv_path=project_root / '.env')

# Add the project directory to the sys.path
sys.path.append(os.path.abspath(project_root))
project = 'Goit Python Web HW 14'
copyright = '2024, Yaroslav Kubitskyi'
author = 'Yaroslav Kubitskyi'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


language = 'uk_UA'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'nature'
html_static_path = ['_static']
