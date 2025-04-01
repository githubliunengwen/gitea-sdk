"""
Reactions module for the Gitea Issues SDK.

This module provides functionality for working with reactions to issues and comments in Gitea repositories.
"""

from .api import ReactionsAPI
from .models import Reaction, EditReactionOption

__all__ = ["ReactionsAPI", "Reaction", "EditReactionOption"]
