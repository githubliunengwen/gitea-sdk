"""
Labels module for the Gitea Issues SDK.

This module provides functionality for working with issue labels in Gitea repositories.
"""

from .api import LabelsAPI
from .models import Label, CreateLabelOption, EditLabelOption

__all__ = ["LabelsAPI", "Label", "CreateLabelOption", "EditLabelOption"]
