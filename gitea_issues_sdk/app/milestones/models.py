"""Data models for Gitea issue milestones."""

from datetime import datetime
from typing import Optional


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
        self.due_on = self._parse_date(data.get("due_on"))
        self.created_at = self._parse_date(data.get("created_at"))
        self.updated_at = self._parse_date(data.get("updated_at"))
        self.closed_at = self._parse_date(data.get("closed_at"))
        self.closed_issues = data.get("closed_issues")
        self.open_issues = data.get("open_issues")
        self.total_issues = data.get("total_issues")

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object."""
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                return None
        return None

    def __str__(self):
        return self.title


class CreateMilestoneOption:
    """Options for creating a milestone."""

    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        state: Optional[str] = None,
        due_on: Optional[datetime] = None,
    ):
        """Initialize options for creating a milestone.

        Args:
            title: Milestone title
            description: Milestone description
            state: Milestone state (open, closed)
            due_on: Milestone due date
        """
        self.title = title
        self.description = description
        self.state = state
        self.due_on = due_on

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        data = {"title": self.title}
        
        if self.description is not None:
            data["description"] = self.description
        if self.state is not None:
            data["state"] = self.state
        if self.due_on is not None:
            data["due_on"] = self.due_on.isoformat()
            
        return data


class EditMilestoneOption:
    """Options for editing a milestone."""

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        state: Optional[str] = None,
        due_on: Optional[datetime] = None,
    ):
        """Initialize options for editing a milestone.

        Args:
            title: New milestone title
            description: New milestone description
            state: New milestone state (open, closed)
            due_on: New milestone due date
        """
        self.title = title
        self.description = description
        self.state = state
        self.due_on = due_on

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        data = {}
        
        if self.title is not None:
            data["title"] = self.title
        if self.description is not None:
            data["description"] = self.description
        if self.state is not None:
            data["state"] = self.state
        if self.due_on is not None:
            data["due_on"] = self.due_on.isoformat()
            
        return data
