# Import config class:
from .apps import DjangotextsplitterConfig

# NOTE: This file should initialize the config-class, but not any models!
# The trick for making something a Django-package is to fisrt make it
# a python package (exactly as you normally would) and then, inside
# the app-folder: put in an init-file which only adds the Config-class
# for that app, but nothing else. No models, loads, deletes of any kind.
# then, simply add it in the Django of your choice under
# INSTALLED_APPS & urls as you normally would. The Config-class needs to
# be python-importable so django can find it. Once Django runs this, you have access
# to anything inside the app, even if it is located inside the venv.
