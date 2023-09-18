import sys
import os

sys.path.append(os.path.abspath("..."))
project = "kulyk-goit-pythonweb-hw-12"
copyright = "2023, kulyk"
author = "kulyk"


extensions = ["sphinx.ext.autodoc"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "nature"
html_static_path = ["_static"]
