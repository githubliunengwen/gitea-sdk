"""
Blocks module for the Gitea Issues SDK.

This module provides functionality for working with issue blocking relationships in Gitea repositories.
"""

from .api import BlocksAPI
from .models import IssueMeta

__all__ = ["BlocksAPI", "IssueMeta"]
