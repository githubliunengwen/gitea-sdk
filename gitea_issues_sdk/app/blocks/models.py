"""Data models for Gitea issue blocking relationships."""

from typing import Optional


class IssueMeta:
    """Model representing issue metadata for blocking relationships."""

    def __init__(
        self,
        owner: str,
        repo: str,
        index: int,
    ):
        """Initialize an IssueMeta object.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
        """
        self.owner = owner
        self.repo = repo
        self.index = index

    def to_dict(self) -> dict:
        """Convert the object to a dictionary for the API request.

        Returns:
            Dictionary representation of the object
        """
        return {
            "owner": self.owner,
            "repo": self.repo,
            "index": self.index,
        }
