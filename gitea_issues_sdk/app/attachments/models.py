"""Data models for Gitea issue and comment attachments."""

from typing import Optional


class Attachment:
    """Model representing a Gitea attachment."""

    def __init__(self, data: dict):
        """Initialize an Attachment object from API data.

        Args:
            data: Attachment data from the API
        """
        self.id = data.get("id")
        self.name = data.get("name")
        self.size = data.get("size")
        self.download_url = data.get("download_url")
        self.uuid = data.get("uuid")
        self.browser_download_url = data.get("browser_download_url")
        self.created_at = data.get("created_at")

    def __str__(self):
        return f"{self.name} ({self.size} bytes)"


class EditAttachmentOption:
    """Options for editing an attachment."""

    def __init__(
        self,
        name: Optional[str] = None,
    ):
        """Initialize options for editing an attachment.

        Args:
            name: New attachment name
        """
        self.name = name

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        data = {}
        
        if self.name is not None:
            data["name"] = self.name
            
        return data
