"""
Milestones module for the Gitea Issues SDK.

This module provides functionality for working with issue milestones in Gitea repositories.
"""

from .api import MilestonesAPI
from .models import Milestone, CreateMilestoneOption, EditMilestoneOption

__all__ = ["MilestonesAPI", "Milestone", "CreateMilestoneOption", "EditMilestoneOption"]
