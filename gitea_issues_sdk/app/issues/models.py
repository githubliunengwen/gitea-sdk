"""Data models for Gitea issues."""

from datetime import datetime
from typing import List, Optional

from ..common.models import Label, Milestone, RepositoryMeta, User


class PullRequestMeta:
    """Metadata for a pull request."""

    def __init__(self, data: dict = None):
        """Initialize a PullRequestMeta object from API data.

        Args:
            data: Pull request metadata from the API
        """
        if data is None:
            data = {}
        self.merged = data.get("merged")
        self.merged_at = self._parse_date(data.get("merged_at"))

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object."""
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                return None
        return None


class Issue:
    """Model representing a Gitea issue."""

    def __init__(self, data: dict):
        """Initialize an Issue object from API data.

        Args:
            data: Issue data from the API
        """
        self.id = data.get("id")
        self.number = data.get("number")
        self.title = data.get("title")
        self.body = data.get("body")
        self.state = data.get("state")
        self.url = data.get("url")
        self.html_url = data.get("html_url")
        self.comments = data.get("comments", 0)
        
        # Parse user data
        self.user = User(data.get("user", {})) if data.get("user") else None
        
        # Parse assignee data
        self.assignee = User(data.get("assignee", {})) if data.get("assignee") else None
        
        # Parse assignees data
        self.assignees = []
        for assignee_data in data.get("assignees", []):
            self.assignees.append(User(assignee_data))
        
        # Parse milestone data
        self.milestone = Milestone(data.get("milestone", {})) if data.get("milestone") else None
        
        # Parse repository data
        self.repository = RepositoryMeta(data.get("repository", {})) if data.get("repository") else None
        
        # Parse dates
        self.created_at = self._parse_date(data.get("created_at"))
        self.updated_at = self._parse_date(data.get("updated_at"))
        self.closed_at = self._parse_date(data.get("closed_at"))
        self.due_date = self._parse_date(data.get("due_date"))
        
        # Parse pull request data
        self.pull_request = PullRequestMeta(data.get("pull_request", {})) if data.get("pull_request") else None
        
        # Parse labels
        self.labels = []
        for label_data in data.get("labels", []):
            self.labels.append(Label(label_data))
        
        self.is_locked = data.get("is_locked", False)
        self.pin_order = data.get("pin_order")
        self.ref = data.get("ref")

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse a date string into a datetime object."""
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                return None
        return None

    def __str__(self):
        return f"#{self.number}: {self.title}"


class CreateIssueOption:
    """Options for creating an issue."""

    def __init__(
        self,
        title: str,
        body: Optional[str] = None,
        assignee: Optional[str] = None,
        assignees: Optional[List[str]] = None,
        milestone: Optional[int] = None,
        labels: Optional[List[str]] = None,
        deadline: Optional[datetime] = None,
        ref: Optional[str] = None,
    ):
        """Initialize options for creating an issue.

        Args:
            title: Issue title
            body: Issue body
            assignee: Username of assignee
            assignees: Usernames of assignees
            milestone: Milestone ID
            labels: Label names
            deadline: Due date
            ref: Git reference
        """
        self.title = title
        self.body = body
        self.assignee = assignee
        self.assignees = assignees
        self.milestone = milestone
        self.labels = labels
        self.deadline = deadline
        self.ref = ref

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        data = {"title": self.title}
        
        if self.body is not None:
            data["body"] = self.body
        if self.assignee is not None:
            data["assignee"] = self.assignee
        if self.assignees is not None:
            data["assignees"] = self.assignees
        if self.milestone is not None:
            data["milestone"] = self.milestone
        if self.labels is not None:
            data["labels"] = self.labels
        if self.deadline is not None:
            data["deadline"] = self.deadline.isoformat()
        if self.ref is not None:
            data["ref"] = self.ref
            
        return data


class EditIssueOption:
    """Options for editing an issue."""

    def __init__(
        self,
        title: Optional[str] = None,
        body: Optional[str] = None,
        assignee: Optional[str] = None,
        assignees: Optional[List[str]] = None,
        milestone: Optional[int] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        deadline: Optional[datetime] = None,
        ref: Optional[str] = None,
    ):
        """Initialize options for editing an issue.

        Args:
            title: New title
            body: New body
            assignee: New assignee
            assignees: New assignees
            milestone: New milestone ID
            state: New state
            labels: New labels
            deadline: New due date
            ref: New Git reference
        """
        self.title = title
        self.body = body
        self.assignee = assignee
        self.assignees = assignees
        self.milestone = milestone
        self.state = state
        self.labels = labels
        self.deadline = deadline
        self.ref = ref

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        data = {}
        
        if self.title is not None:
            data["title"] = self.title
        if self.body is not None:
            data["body"] = self.body
        if self.assignee is not None:
            data["assignee"] = self.assignee
        if self.assignees is not None:
            data["assignees"] = self.assignees
        if self.milestone is not None:
            data["milestone"] = self.milestone
        if self.state is not None:
            data["state"] = self.state
        if self.labels is not None:
            data["labels"] = self.labels
        if self.deadline is not None:
            data["deadline"] = self.deadline.isoformat()
        if self.ref is not None:
            data["ref"] = self.ref
            
        return data
