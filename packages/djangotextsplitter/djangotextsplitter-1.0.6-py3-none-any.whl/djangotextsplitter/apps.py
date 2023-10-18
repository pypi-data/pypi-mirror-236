"""
Module to define the Config-class.
"""

from django.apps import AppConfig


class DjangotextsplitterConfig(AppConfig):
    """
    This class is used by django to initialize the application.
    As such, it should be made available in __init__.py
    when packaging an app (such as this one).
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "djangotextsplitter"
