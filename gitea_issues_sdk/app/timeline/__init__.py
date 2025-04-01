"""
Timeline module for the Gitea Issues SDK.

This module provides functionality for working with issue timelines in Gitea repositories.
"""

from .api import TimelineAPI
from .models import TimelineEvent

__all__ = ["TimelineAPI", "TimelineEvent"]
