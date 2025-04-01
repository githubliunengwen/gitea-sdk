"""Data models for Gitea reactions."""

from typing import Optional

from ..common.models import User


class Reaction:
    """Model representing a Gitea reaction."""

    def __init__(self, data: dict):
        """Initialize a Reaction object from API data.

        Args:
            data: Reaction data from the API
        """
        self.id = data.get("id")
        self.user_id = data.get("user_id")
        self.content = data.get("content")
        self.created_at = data.get("created_at")
        
        # Parse user data
        self.user = User(data.get("user", {})) if data.get("user") else None

    def __str__(self):
        return f"{self.content} by {self.user.username if self.user else 'Unknown'}"


class EditReactionOption:
    """Options for adding a reaction."""

    def __init__(self, content: str):
        """Initialize options for adding a reaction.

        Args:
            content: Reaction content (e.g., "+1", "-1", "laugh", "confused", "heart", "hooray", "eyes", "rocket")
        """
        self.content = content

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        return {"content": self.content}
