"""Utility functions for working with Gitea issue labels."""

import logging
from typing import Dict, List, Optional

from .models import Label

logger = logging.getLogger("gitea_issues_sdk")


def filter_labels_by_color(labels: List[Label], color: str) -> List[Label]:
    """Filter labels by color.

    Args:
        labels: List of labels to filter
        color: Color to filter by (hex code without #)

    Returns:
        Filtered list of labels
    """
    color = color.lstrip("#")  # Remove # if present
    logger.debug(f"Filtering labels by color: {color}")
    return [label for label in labels if label.color and label.color.lower() == color.lower()]


def filter_labels_by_name_contains(labels: List[Label], text: str) -> List[Label]:
    """Filter labels by name containing text.

    Args:
        labels: List of labels to filter
        text: Text to search for in label names

    Returns:
        Filtered list of labels
    """
    logger.debug(f"Filtering labels by name containing: {text}")
    return [label for label in labels if text.lower() in label.name.lower()]


def sort_labels_by_name(labels: List[Label], ascending: bool = True) -> List[Label]:
    """Sort labels by name.

    Args:
        labels: List of labels to sort
        ascending: Sort in ascending order if True, descending if False

    Returns:
        Sorted list of labels
    """
    logger.debug(f"Sorting labels by name (ascending={ascending})")
    return sorted(labels, key=lambda label: label.name.lower(), reverse=not ascending)


def group_labels_by_color(labels: List[Label]) -> Dict[str, List[Label]]:
    """Group labels by color.

    Args:
        labels: List of labels to group

    Returns:
        Dictionary with colors as keys and lists of labels as values
    """
    logger.debug("Grouping labels by color")
    result: Dict[str, List[Label]] = {}
    
    for label in labels:
        color = label.color or "unknown"
        
        if color not in result:
            result[color] = []
            
        result[color].append(label)
        
    return result


def format_label_summary(label: Label) -> str:
    """Format a label as a summary string.

    Args:
        label: Label to format

    Returns:
        Formatted label summary
    """
    summary = f"{label.name}"
    
    if label.color:
        summary += f" (#{label.color})"
        
    if label.description:
        summary += f": {label.description}"
        
    return summary
