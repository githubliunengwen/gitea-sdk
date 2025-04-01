"""Data models for Gitea issue stopwatches and tracked time."""

from datetime import datetime
from typing import Optional


class TrackedTime:
    """Model representing tracked time on an issue."""

    def __init__(self, data: dict):
        """Initialize a TrackedTime object from API data.

        Args:
            data: Tracked time data from the API
        """
        self.id = data.get("id")
        self.issue_id = data.get("issue_id")
        self.user_id = data.get("user_id")
        self.created = self._parse_date(data.get("created"))
        self.time = data.get("time")  # Time in seconds
        self.user_name = data.get("user_name")
        
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object."""
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                return None
        return None
        
    def get_hours(self) -> float:
        """Get the tracked time in hours.

        Returns:
            Tracked time in hours
        """
        if self.time is not None:
            return self.time / 3600.0
        return 0.0
        
    def get_formatted_time(self) -> str:
        """Get the tracked time in a human-readable format.

        Returns:
            Tracked time in format "Xh Ym"
        """
        if self.time is None:
            return "0h 0m"
            
        hours = int(self.time // 3600)
        minutes = int((self.time % 3600) // 60)
        return f"{hours}h {minutes}m"
        
    def __str__(self):
        username = self.user_name or f"User {self.user_id}"
        return f"{self.get_formatted_time()} tracked by {username} on {self.created}"
