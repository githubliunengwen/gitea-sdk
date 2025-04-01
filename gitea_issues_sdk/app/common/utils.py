"""Common utility functions for the Gitea Issues SDK."""

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger("gitea_issues_sdk")


def setup_logger(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """Set up the logger for the SDK.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (if None, logs to console only)
        log_format: Log format string

    Returns:
        Configured logger
    """
    # Set default log format if not provided
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Get the logger
    logger = logging.getLogger("gitea_issues_sdk")

    # Set log level
    level_upper = level.upper()
    numeric_level = getattr(logging, level_upper, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    logger.setLevel(numeric_level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if log_file is provided
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def validate_repo_path(owner: str, repo: str) -> bool:
    """Validate repository owner and name.

    Args:
        owner: Repository owner
        repo: Repository name

    Returns:
        True if valid, False otherwise
    """
    # Check if owner and repo are not empty
    if not owner or not repo:
        return False

    # Check if owner and repo contain only valid characters
    # Gitea allows alphanumeric characters, hyphens, underscores, and dots
    pattern = r"^[a-zA-Z0-9_.-]+$"
    return bool(re.match(pattern, owner) and re.match(pattern, repo))


def parse_iso_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """Parse an ISO 8601 datetime string into a datetime object.

    Args:
        date_str: ISO 8601 datetime string

    Returns:
        Datetime object or None if parsing fails
    """
    if not date_str:
        return None

    try:
        # Handle 'Z' timezone indicator
        if date_str.endswith("Z"):
            date_str = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(date_str)
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to parse datetime: {date_str} - {e}")
        return None


def format_datetime(dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[str]:
    """Format a datetime object as a string.

    Args:
        dt: Datetime object
        format_str: Format string

    Returns:
        Formatted datetime string or None if dt is None
    """
    if dt is None:
        return None
    return dt.strftime(format_str)


def filter_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Filter out None values from a dictionary.

    Args:
        data: Dictionary to filter

    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in data.items() if v is not None}


def build_query_params(params: Dict[str, Any]) -> Dict[str, str]:
    """Build query parameters for API requests.

    Args:
        params: Dictionary of parameters

    Returns:
        Dictionary of query parameters with values converted to strings
    """
    result = {}
    for key, value in params.items():
        if value is None:
            continue
        elif isinstance(value, bool):
            result[key] = str(value).lower()
        elif isinstance(value, (list, tuple)):
            result[key] = ",".join(str(item) for item in value)
        elif isinstance(value, datetime):
            result[key] = value.isoformat()
        else:
            result[key] = str(value)
    return result


def paginate_results(
    fetch_func: callable,
    page_size: int = 30,
    max_items: Optional[int] = None,
    **kwargs: Any,
) -> List[Any]:
    """Paginate through API results.

    Args:
        fetch_func: Function to fetch a page of results
        page_size: Number of items per page
        max_items: Maximum number of items to return
        **kwargs: Additional arguments to pass to fetch_func

    Returns:
        List of all items
    """
    results = []
    page = 1
    
    while True:
        # Fetch a page of results
        page_results = fetch_func(page=page, limit=page_size, **kwargs)
        
        # If no results, we've reached the end
        if not page_results:
            break
            
        # Add results to the list
        results.extend(page_results)
        
        # If we've reached the maximum number of items, stop
        if max_items and len(results) >= max_items:
            results = results[:max_items]
            break
            
        # If we got fewer results than the page size, we've reached the end
        if len(page_results) < page_size:
            break
            
        # Move to the next page
        page += 1
        
    return results
