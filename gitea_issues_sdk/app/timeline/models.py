"""Data models for Gitea issue timeline events."""

from datetime import datetime
from typing import Optional, Dict, Any

from ..common.models import User


class TimelineEvent:
    """Model representing a Gitea issue timeline event."""

    def __init__(self, data: dict):
        """Initialize a TimelineEvent object from API data.

        Args:
            data: Timeline event data from the API
        """
        self.id = data.get("id")
        self.type = data.get("type")
        self.created_at = self._parse_date(data.get("created_at"))
        
        # Parse user data
        self.user = User(data.get("user", {})) if data.get("user") else None
        
        # Parse assignee data if present
        self.assignee = User(data.get("assignee", {})) if data.get("assignee") else None
        
        # Parse label data if present
        self.label = data.get("label")
        
        # Parse milestone data if present
        self.milestone = data.get("milestone")
        
        # Parse comment data if present
        self.comment = data.get("comment")
        
        # Parse commit data if present
        self.commit = data.get("commit")
        
        # Parse ref data if present
        self.ref = data.get("ref")
        self.ref_action = data.get("ref_action")
        
        # Parse review data if present
        self.review = data.get("review")
        
        # Parse tracked time data if present
        self.tracked_time = data.get("tracked_time")
        
        # Store the original data for any fields not explicitly parsed
        self._raw_data = data

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object."""
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                return None
        return None

    def get_raw_data(self) -> Dict[str, Any]:
        """Get the raw data for this event.

        Returns:
            Raw data dictionary
        """
        return self._raw_data

    def __str__(self):
        event_type = self.type or "Unknown"
        username = self.user.username if self.user else "Unknown"
        return f"{event_type} by {username} at {self.created_at}"
