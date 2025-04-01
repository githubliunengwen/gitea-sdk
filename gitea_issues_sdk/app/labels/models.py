"""Data models for Gitea issue labels."""

from typing import Optional


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
        self.exclusive = data.get("exclusive", False)
        self.is_archived = data.get("is_archived", False)

    def __str__(self):
        return self.name


class CreateLabelOption:
    """Options for creating a label."""

    def __init__(
        self,
        name: str,
        color: str,
        description: Optional[str] = None,
        exclusive: bool = False,
    ):
        """Initialize options for creating a label.

        Args:
            name: Label name
            color: Label color (hex code without #)
            description: Label description
            exclusive: Whether the label is exclusive
        """
        self.name = name
        self.color = color.lstrip("#")  # Remove # if present
        self.description = description
        self.exclusive = exclusive

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        data = {
            "name": self.name,
            "color": self.color,
        }
        
        if self.description is not None:
            data["description"] = self.description
        
        data["exclusive"] = self.exclusive
            
        return data


class EditLabelOption:
    """Options for editing a label."""

    def __init__(
        self,
        name: Optional[str] = None,
        color: Optional[str] = None,
        description: Optional[str] = None,
        exclusive: Optional[bool] = None,
    ):
        """Initialize options for editing a label.

        Args:
            name: New label name
            color: New label color (hex code without #)
            description: New label description
            exclusive: Whether the label is exclusive
        """
        self.name = name
        self.color = color.lstrip("#") if color else None
        self.description = description
        self.exclusive = exclusive

    def to_dict(self) -> dict:
        """Convert the options to a dictionary for the API request.

        Returns:
            Dictionary representation of the options
        """
        data = {}
        
        if self.name is not None:
            data["name"] = self.name
        if self.color is not None:
            data["color"] = self.color
        if self.description is not None:
            data["description"] = self.description
        if self.exclusive is not None:
            data["exclusive"] = self.exclusive
            
        return data
