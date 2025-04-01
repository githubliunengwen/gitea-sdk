"""Common data models for the Gitea API."""

from datetime import datetime
from typing import List, Optional

class User:
    """Model representing a Gitea user."""

    def __init__(self, data: dict):
        """Initialize a User object from API data.

        Args:
            data: User data from the API
        """
        self.id = data.get("id")
        self.login = data.get("login")
        self.full_name = data.get("full_name")
        self.email = data.get("email")
        self.avatar_url = data.get("avatar_url")
        self.username = data.get("username")

    def __str__(self):
        return f"{self.username} ({self.full_name})" if self.full_name else self.username


class RepositoryMeta:
    """Basic repository information."""

    def __init__(self, data: dict):
        """Initialize a RepositoryMeta object from API data.

        Args:
            data: Repository data from the API
        """
        self.id = data.get("id")
        self.name = data.get("name")
        self.owner = data.get("owner")
        self.full_name = data.get("full_name")

    def __str__(self):
        return self.full_name


class Label:
    """Model representing a Gitea label."""

    def __init__(self, data: dict):
        """Initialize a Label object from API data.

        Args:
            data: Label data from the API
        """
        self.id = data.get("id")
        self.name = data.get("name")
        self.color = data.get("color")
        self.description = data.get("description")
        self.url = data.get("url")

    def __str__(self):
        return self.name


class Milestone:
    """Model representing a Gitea milestone."""

    def __init__(self, data: dict):
        """Initialize a Milestone object from API data.

        Args:
            data: Milestone data from the API
        """
        self.id = data.get("id")
        self.title = data.get("title")
        self.description = data.get("description")
        self.state = data.get("state")
        self.open_issues = data.get("open_issues")
        self.closed_issues = data.get("closed_issues")
        
        # Parse dates
        self.created_at = self._parse_date(data.get("created_at"))
        self.updated_at = self._parse_date(data.get("updated_at"))
        self.closed_at = self._parse_date(data.get("closed_at"))
        self.due_on = self._parse_date(data.get("due_on"))

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object.

        Args:
            date_str: Date string from the API

        Returns:
            Datetime object or None if date_str is None
        """
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                return None
        return None

    def __str__(self):
        return self.title


class Attachment:
    """Model representing a file attachment."""

    def __init__(self, data: dict):
        """Initialize an Attachment object from API data.

        Args:
            data: Attachment data from the API
        """
        self.id = data.get("id")
        self.name = data.get("name")
        self.size = data.get("size")
        self.download_count = data.get("download_count")
        self.created_at = self._parse_date(data.get("created"))
        self.uuid = data.get("uuid")
        self.browser_download_url = data.get("browser_download_url")

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object.

        Args:
            date_str: Date string from the API

        Returns:
            Datetime object or None if date_str is None
        """
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                return None
        return None

    def __str__(self):
        return self.name
