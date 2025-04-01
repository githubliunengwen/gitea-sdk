"""Data models for Gitea issue comments."""

from datetime import datetime
from typing import List, Optional

from ..common.models import Attachment, User


class Comment:
    """Model representing a Gitea issue comment."""

    def __init__(self, data: dict):
        """Initialize a Comment object from API data.

        Args:
            data: Comment data from the API
        """
        self.id = data.get("id")
        self.body = data.get("body")
        self.html_url = data.get("html_url")
        self.pull_request_url = data.get("pull_request_url")
        self.issue_url = data.get("issue_url")
        
        # Parse user data
        self.user = User(data.get("user", {})) if data.get("user") else None
        
        # Parse dates
        self.created_at = self._parse_date(data.get("created_at"))
        self.updated_at = self._parse_date(data.get("updated_at"))
        
        # Parse attachments
        self.attachments = []
        for attachment_data in data.get("attachments", []):
            self.attachments.append(Attachment(attachment_data))

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object."""
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                return None
        return None

    def __str__(self):
        return f"Comment by {self.user.username if self.user else 'Unknown'}"


class CreateCommentOption:
    """Options for creating a comment."""

    def __init__(self, body: str):
        """Initialize options for creating a comment.

        Args:
            body: Comment body
        """
        self.body = body

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        return {"body": self.body}


class EditCommentOption:
    """Options for editing a comment."""

    def __init__(self, body: str):
        """Initialize options for editing a comment.

        Args:
            body: New comment body
        """
        self.body = body

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        return {"body": self.body}
