"""Utility functions for working with Gitea issues."""

import logging
from typing import Dict, List, Optional, Union

from .models import Issue

logger = logging.getLogger("gitea_issues_sdk")


def filter_issues_by_label(issues: List[Issue], label_name: str) -> List[Issue]:
    """Filter issues by label name.

    Args:
        issues: List of issues to filter
        label_name: Label name to filter by

    Returns:
        Filtered list of issues
    """
    logger.debug(f"Filtering issues by label: {label_name}")
    return [issue for issue in issues if any(label.name == label_name for label in issue.labels)]


def filter_issues_by_state(issues: List[Issue], state: str) -> List[Issue]:
    """Filter issues by state.

    Args:
        issues: List of issues to filter
        state: State to filter by (open, closed)

    Returns:
        Filtered list of issues
    """
    logger.debug(f"Filtering issues by state: {state}")
    return [issue for issue in issues if issue.state == state]


def filter_issues_by_assignee(issues: List[Issue], username: str) -> List[Issue]:
    """Filter issues by assignee username.

    Args:
        issues: List of issues to filter
        username: Assignee username to filter by

    Returns:
        Filtered list of issues
    """
    logger.debug(f"Filtering issues by assignee: {username}")
    return [
        issue for issue in issues 
        if issue.assignee and issue.assignee.username == username
        or any(assignee.username == username for assignee in issue.assignees)
    ]


def group_issues_by_milestone(issues: List[Issue]) -> Dict[str, List[Issue]]:
    """Group issues by milestone.

    Args:
        issues: List of issues to group

    Returns:
        Dictionary with milestone titles as keys and lists of issues as values
    """
    logger.debug("Grouping issues by milestone")
    result: Dict[str, List[Issue]] = {}
    
    for issue in issues:
        if not issue.milestone:
            milestone_title = "No Milestone"
        else:
            milestone_title = issue.milestone.title
            
        if milestone_title not in result:
            result[milestone_title] = []
            
        result[milestone_title].append(issue)
        
    return result


def sort_issues_by_created_date(issues: List[Issue], ascending: bool = True) -> List[Issue]:
    """Sort issues by creation date.

    Args:
        issues: List of issues to sort
        ascending: Sort in ascending order if True, descending if False

    Returns:
        Sorted list of issues
    """
    logger.debug(f"Sorting issues by created date (ascending={ascending})")
    return sorted(issues, key=lambda issue: issue.created_at, reverse=not ascending)


def sort_issues_by_updated_date(issues: List[Issue], ascending: bool = True) -> List[Issue]:
    """Sort issues by last updated date.

    Args:
        issues: List of issues to sort
        ascending: Sort in ascending order if True, descending if False

    Returns:
        Sorted list of issues
    """
    logger.debug(f"Sorting issues by updated date (ascending={ascending})")
    return sorted(issues, key=lambda issue: issue.updated_at, reverse=not ascending)


def format_issue_summary(issue: Issue) -> str:
    """Format an issue as a summary string.

    Args:
        issue: Issue to format

    Returns:
        Formatted issue summary
    """
    summary = f"#{issue.number}: {issue.title}"
    
    if issue.state:
        summary += f" [{issue.state}]"
        
    if issue.assignee:
        summary += f" (assigned to {issue.assignee.username})"
        
    if issue.labels:
        label_names = [label.name for label in issue.labels]
        summary += f" - Labels: {', '.join(label_names)}"
        
    return summary
