"""Utility functions for working with Gitea issue comments."""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from .models import Comment

logger = logging.getLogger("gitea_issues_sdk")


def filter_comments_by_user(comments: List[Comment], username: str) -> List[Comment]:
    """Filter comments by user.

    Args:
        comments: List of comments to filter
        username: Username to filter by

    Returns:
        Filtered list of comments
    """
    logger.debug(f"Filtering comments by user: {username}")
    return [comment for comment in comments if comment.user and comment.user.username == username]


def filter_comments_by_date_range(
    comments: List[Comment],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[Comment]:
    """Filter comments by date range.

    Args:
        comments: List of comments to filter
        start_date: Start date for filtering (inclusive)
        end_date: End date for filtering (inclusive)

    Returns:
        Filtered list of comments
    """
    filtered_comments = comments
    
    if start_date:
        logger.debug(f"Filtering comments after: {start_date.isoformat()}")
        filtered_comments = [
            comment for comment in filtered_comments 
            if comment.created_at and comment.created_at >= start_date
        ]
        
    if end_date:
        logger.debug(f"Filtering comments before: {end_date.isoformat()}")
        filtered_comments = [
            comment for comment in filtered_comments 
            if comment.created_at and comment.created_at <= end_date
        ]
        
    return filtered_comments


def sort_comments_by_date(comments: List[Comment], ascending: bool = True) -> List[Comment]:
    """Sort comments by creation date.

    Args:
        comments: List of comments to sort
        ascending: Sort in ascending order if True, descending if False

    Returns:
        Sorted list of comments
    """
    logger.debug(f"Sorting comments by date (ascending={ascending})")
    return sorted(comments, key=lambda comment: comment.created_at, reverse=not ascending)


def group_comments_by_user(comments: List[Comment]) -> Dict[str, List[Comment]]:
    """Group comments by user.

    Args:
        comments: List of comments to group

    Returns:
        Dictionary with usernames as keys and lists of comments as values
    """
    logger.debug("Grouping comments by user")
    result: Dict[str, List[Comment]] = {}
    
    for comment in comments:
        if not comment.user:
            username = "Unknown"
        else:
            username = comment.user.username
            
        if username not in result:
            result[username] = []
            
        result[username].append(comment)
        
    return result


def format_comment_summary(comment: Comment) -> str:
    """Format a comment as a summary string.

    Args:
        comment: Comment to format

    Returns:
        Formatted comment summary
    """
    username = comment.user.username if comment.user else "Unknown"
    created_at = comment.created_at.strftime("%Y-%m-%d %H:%M:%S") if comment.created_at else "Unknown date"
    
    summary = f"Comment by {username} on {created_at}"
    
    if comment.body:
        # Truncate body if it's too long
        body = comment.body[:100] + "..." if len(comment.body) > 100 else comment.body
        # Replace newlines with spaces for a cleaner summary
        body = body.replace("\n", " ")
        summary += f": {body}"
        
    return summary


def has_attachments(comment: Comment) -> bool:
    """Check if a comment has attachments.

    Args:
        comment: Comment to check

    Returns:
        True if the comment has attachments, False otherwise
    """
    return len(comment.attachments) > 0
