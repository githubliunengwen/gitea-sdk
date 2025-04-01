"""Utility functions for working with Gitea issue milestones."""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from .models import Milestone

logger = logging.getLogger("gitea_issues_sdk")


def filter_milestones_by_state(milestones: List[Milestone], state: str) -> List[Milestone]:
    """Filter milestones by state.

    Args:
        milestones: List of milestones to filter
        state: State to filter by (open, closed)

    Returns:
        Filtered list of milestones
    """
    logger.debug(f"Filtering milestones by state: {state}")
    return [milestone for milestone in milestones if milestone.state == state]


def filter_milestones_by_due_date(
    milestones: List[Milestone],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[Milestone]:
    """Filter milestones by due date range.

    Args:
        milestones: List of milestones to filter
        start_date: Start date for filtering (inclusive)
        end_date: End date for filtering (inclusive)

    Returns:
        Filtered list of milestones
    """
    filtered_milestones = milestones
    
    if start_date:
        logger.debug(f"Filtering milestones due after: {start_date.isoformat()}")
        filtered_milestones = [
            milestone for milestone in filtered_milestones 
            if milestone.due_on and milestone.due_on >= start_date
        ]
        
    if end_date:
        logger.debug(f"Filtering milestones due before: {end_date.isoformat()}")
        filtered_milestones = [
            milestone for milestone in filtered_milestones 
            if milestone.due_on and milestone.due_on <= end_date
        ]
        
    return filtered_milestones


def sort_milestones_by_due_date(milestones: List[Milestone], ascending: bool = True) -> List[Milestone]:
    """Sort milestones by due date.

    Args:
        milestones: List of milestones to sort
        ascending: Sort in ascending order if True, descending if False

    Returns:
        Sorted list of milestones
    """
    logger.debug(f"Sorting milestones by due date (ascending={ascending})")
    
    # Handle milestones without due dates by placing them at the end
    def get_due_date(milestone):
        return milestone.due_on or datetime.max
        
    return sorted(milestones, key=get_due_date, reverse=not ascending)


def sort_milestones_by_completion(milestones: List[Milestone], ascending: bool = True) -> List[Milestone]:
    """Sort milestones by completion percentage.

    Args:
        milestones: List of milestones to sort
        ascending: Sort in ascending order if True, descending if False

    Returns:
        Sorted list of milestones
    """
    logger.debug(f"Sorting milestones by completion percentage (ascending={ascending})")
    
    def get_completion_percentage(milestone):
        if milestone.total_issues == 0:
            return 0
        return (milestone.closed_issues / milestone.total_issues) * 100
        
    return sorted(milestones, key=get_completion_percentage, reverse=not ascending)


def get_active_milestones(milestones: List[Milestone]) -> List[Milestone]:
    """Get active milestones (open and with a due date in the future).

    Args:
        milestones: List of milestones to filter

    Returns:
        List of active milestones
    """
    logger.debug("Getting active milestones")
    now = datetime.now()
    return [
        milestone for milestone in milestones
        if milestone.state == "open" and (milestone.due_on is None or milestone.due_on > now)
    ]


def get_overdue_milestones(milestones: List[Milestone]) -> List[Milestone]:
    """Get overdue milestones (open and with a due date in the past).

    Args:
        milestones: List of milestones to filter

    Returns:
        List of overdue milestones
    """
    logger.debug("Getting overdue milestones")
    now = datetime.now()
    return [
        milestone for milestone in milestones
        if milestone.state == "open" and milestone.due_on and milestone.due_on < now
    ]


def format_milestone_summary(milestone: Milestone) -> str:
    """Format a milestone as a summary string.

    Args:
        milestone: Milestone to format

    Returns:
        Formatted milestone summary
    """
    summary = f"{milestone.title}"
    
    if milestone.state:
        summary += f" [{milestone.state}]"
        
    if milestone.due_on:
        summary += f" (due: {milestone.due_on.strftime('%Y-%m-%d')})"
        
    if milestone.total_issues is not None and milestone.total_issues > 0:
        completion = (milestone.closed_issues or 0) / milestone.total_issues * 100
        summary += f" - {completion:.1f}% complete"
        
    return summary
