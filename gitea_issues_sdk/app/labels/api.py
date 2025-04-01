"""API client for Gitea issue labels."""

import logging
from typing import Dict, List, Optional, Union

from ..client import GiteaClient
from .models import Label, CreateLabelOption, EditLabelOption

logger = logging.getLogger("gitea_issues_sdk")


class LabelsAPI:
    """API client for working with Gitea issue labels."""

    def __init__(self, client: GiteaClient):
        """Initialize the labels API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_labels(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Label]:
        """List labels in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            page: Page number
            limit: Page size

        Returns:
            List of labels in the repository
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing labels for {owner}/{repo} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/labels", params=params)
        
        labels = []
        for label_data in response:
            try:
                labels.append(Label(label_data))
            except Exception as e:
                logger.error(f"Error parsing label data: {e}")
                
        return labels

    def get_label(self, owner: str, repo: str, id: int) -> Label:
        """Get a specific label.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Label ID

        Returns:
            The label

        Raises:
            GiteaAPIError: If the label doesn't exist
        """
        logger.debug(f"Getting label {owner}/{repo}#{id}")
        response = self.client.get(f"repos/{owner}/{repo}/labels/{id}")
        return Label(response)

    def create_label(
        self,
        owner: str,
        repo: str,
        name: str,
        color: str,
        description: Optional[str] = None,
        exclusive: bool = False,
    ) -> Label:
        """Create a new label.

        Args:
            owner: Repository owner
            repo: Repository name
            name: Label name
            color: Label color (hex code)
            description: Label description
            exclusive: Whether the label is exclusive

        Returns:
            The created label

        Raises:
            GiteaAPIError: If the label couldn't be created
        """
        label_data = CreateLabelOption(
            name=name,
            color=color,
            description=description,
            exclusive=exclusive,
        )
        
        logger.debug(f"Creating label in {owner}/{repo}: {name}")
        response = self.client.post(
            f"repos/{owner}/{repo}/labels",
            json_data=label_data.to_dict(),
        )
        
        return Label(response)

    def edit_label(
        self,
        owner: str,
        repo: str,
        id: int,
        name: Optional[str] = None,
        color: Optional[str] = None,
        description: Optional[str] = None,
        exclusive: Optional[bool] = None,
    ) -> Label:
        """Edit an existing label.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Label ID
            name: New label name
            color: New label color (hex code)
            description: New label description
            exclusive: Whether the label is exclusive

        Returns:
            The updated label

        Raises:
            GiteaAPIError: If the label doesn't exist or couldn't be updated
        """
        label_data = EditLabelOption(
            name=name,
            color=color,
            description=description,
            exclusive=exclusive,
        )
        
        logger.debug(f"Editing label {owner}/{repo}#{id}")
        response = self.client.patch(
            f"repos/{owner}/{repo}/labels/{id}",
            json_data=label_data.to_dict(),
        )
        
        return Label(response)

    def delete_label(self, owner: str, repo: str, id: int) -> bool:
        """Delete a label.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Label ID

        Returns:
            True if the label was deleted successfully

        Raises:
            GiteaAPIError: If the label doesn't exist or couldn't be deleted
        """
        logger.debug(f"Deleting label {owner}/{repo}#{id}")
        self.client.delete(f"repos/{owner}/{repo}/labels/{id}")
        return True

    def get_issue_labels(
        self,
        owner: str,
        repo: str,
        index: int,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Label]:
        """Get labels for an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            page: Page number
            limit: Page size

        Returns:
            List of labels for the issue
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Getting labels for issue {owner}/{repo}#{index} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}/labels", params=params)
        
        labels = []
        for label_data in response:
            try:
                labels.append(Label(label_data))
            except Exception as e:
                logger.error(f"Error parsing label data: {e}")
                
        return labels

    def add_issue_label(
        self,
        owner: str,
        repo: str,
        index: int,
        labels: List[int],
    ) -> List[Label]:
        """Add labels to an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            labels: List of label IDs to add

        Returns:
            Updated list of labels for the issue

        Raises:
            GiteaAPIError: If the labels couldn't be added
        """
        logger.debug(f"Adding labels to issue {owner}/{repo}#{index}: {labels}")
        response = self.client.post(
            f"repos/{owner}/{repo}/issues/{index}/labels",
            json_data={"labels": labels},
        )
        
        result_labels = []
        for label_data in response:
            try:
                result_labels.append(Label(label_data))
            except Exception as e:
                logger.error(f"Error parsing label data: {e}")
                
        return result_labels

    def remove_issue_label(
        self,
        owner: str,
        repo: str,
        index: int,
        id: int,
    ) -> bool:
        """Remove a label from an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            id: Label ID to remove

        Returns:
            True if the label was removed successfully

        Raises:
            GiteaAPIError: If the label couldn't be removed
        """
        logger.debug(f"Removing label {id} from issue {owner}/{repo}#{index}")
        self.client.delete(f"repos/{owner}/{repo}/issues/{index}/labels/{id}")
        return True

    def replace_issue_labels(
        self,
        owner: str,
        repo: str,
        index: int,
        labels: List[int],
    ) -> List[Label]:
        """Replace all labels on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            labels: List of label IDs to set

        Returns:
            Updated list of labels for the issue

        Raises:
            GiteaAPIError: If the labels couldn't be replaced
        """
        logger.debug(f"Replacing labels on issue {owner}/{repo}#{index} with: {labels}")
        response = self.client.put(
            f"repos/{owner}/{repo}/issues/{index}/labels",
            json_data={"labels": labels},
        )
        
        result_labels = []
        for label_data in response:
            try:
                result_labels.append(Label(label_data))
            except Exception as e:
                logger.error(f"Error parsing label data: {e}")
                
        return result_labels

    def clear_issue_labels(
        self,
        owner: str,
        repo: str,
        index: int,
    ) -> bool:
        """Remove all labels from an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number

        Returns:
            True if the labels were cleared successfully

        Raises:
            GiteaAPIError: If the labels couldn't be cleared
        """
        logger.debug(f"Clearing labels from issue {owner}/{repo}#{index}")
        self.client.delete(f"repos/{owner}/{repo}/issues/{index}/labels")
        return True
