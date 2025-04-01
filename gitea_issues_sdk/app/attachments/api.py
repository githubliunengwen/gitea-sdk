"""API client for Gitea issue and comment attachments."""

import logging
import os
from typing import Dict, List, Optional, Union, BinaryIO

from ..client import GiteaClient
from .models import Attachment, EditAttachmentOption

logger = logging.getLogger("gitea_issues_sdk")


class AttachmentsAPI:
    """API client for working with Gitea issue and comment attachments."""

    def __init__(self, client: GiteaClient):
        """Initialize the attachments API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_issue_attachments(
        self,
        owner: str,
        repo: str,
        index: int,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Attachment]:
        """List attachments on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            page: Page number
            limit: Page size

        Returns:
            List of attachments on the issue
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing attachments for issue {owner}/{repo}#{index} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}/assets", params=params)
        
        attachments = []
        for attachment_data in response:
            try:
                attachments.append(Attachment(attachment_data))
            except Exception as e:
                logger.error(f"Error parsing attachment data: {e}")
                
        return attachments

    def get_issue_attachment(
        self,
        owner: str,
        repo: str,
        index: int,
        attachment_id: int,
    ) -> Attachment:
        """Get a specific attachment on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            attachment_id: Attachment ID

        Returns:
            The attachment

        Raises:
            GiteaAPIError: If the attachment doesn't exist
        """
        logger.debug(f"Getting attachment {attachment_id} for issue {owner}/{repo}#{index}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}/assets/{attachment_id}")
        return Attachment(response)

    def create_issue_attachment(
        self,
        owner: str,
        repo: str,
        index: int,
        file_path: str,
        file_name: Optional[str] = None,
    ) -> Attachment:
        """Create a new attachment on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            file_path: Path to the file to upload
            file_name: Name to use for the attachment (if None, uses the file's basename)

        Returns:
            The created attachment

        Raises:
            GiteaAPIError: If the attachment couldn't be created
            FileNotFoundError: If the file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if file_name is None:
            file_name = os.path.basename(file_path)
            
        logger.debug(f"Creating attachment for issue {owner}/{repo}#{index}: {file_name}")
        
        response = self.client.post(
            f"repos/{owner}/{repo}/issues/{index}/assets",
            files={'attachment': (file_name, open(file_path, 'rb'))},
        )
            
        return Attachment(response)

    def create_issue_attachment_from_bytes(
        self,
        owner: str,
        repo: str,
        index: int,
        file_content: bytes,
        file_name: str,
    ) -> Attachment:
        """Create a new attachment on an issue from bytes.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            file_content: File content as bytes
            file_name: Name to use for the attachment

        Returns:
            The created attachment

        Raises:
            GiteaAPIError: If the attachment couldn't be created
        """
        logger.debug(f"Creating attachment for issue {owner}/{repo}#{index}: {file_name}")
        
        response = self.client.post(
            f"repos/{owner}/{repo}/issues/{index}/assets",
            files={'attachment': (file_name, file_content)},
        )
            
        return Attachment(response)

    def edit_issue_attachment(
        self,
        owner: str,
        repo: str,
        index: int,
        attachment_id: int,
        name: str,
    ) -> Attachment:
        """Edit an existing attachment on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            attachment_id: Attachment ID
            name: New attachment name

        Returns:
            The updated attachment

        Raises:
            GiteaAPIError: If the attachment doesn't exist or couldn't be updated
        """
        attachment_data = EditAttachmentOption(name=name)
        
        logger.debug(f"Editing attachment {attachment_id} for issue {owner}/{repo}#{index}")
        response = self.client.patch(
            f"repos/{owner}/{repo}/issues/{index}/assets/{attachment_id}",
            json_data=attachment_data.to_dict(),
        )
        
        return Attachment(response)

    def delete_issue_attachment(
        self,
        owner: str,
        repo: str,
        index: int,
        attachment_id: int,
    ) -> bool:
        """Delete an attachment from an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            attachment_id: Attachment ID

        Returns:
            True if the attachment was deleted successfully

        Raises:
            GiteaAPIError: If the attachment doesn't exist or couldn't be deleted
        """
        logger.debug(f"Deleting attachment {attachment_id} from issue {owner}/{repo}#{index}")
        self.client.delete(f"repos/{owner}/{repo}/issues/{index}/assets/{attachment_id}")
        return True

    def list_comment_attachments(
        self,
        owner: str,
        repo: str,
        id: int,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Attachment]:
        """List attachments on a comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID
            page: Page number
            limit: Page size

        Returns:
            List of attachments on the comment
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing attachments for comment {owner}/{repo}#{id} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/comments/{id}/assets", params=params)
        
        attachments = []
        for attachment_data in response:
            try:
                attachments.append(Attachment(attachment_data))
            except Exception as e:
                logger.error(f"Error parsing attachment data: {e}")
                
        return attachments

    def get_comment_attachment(
        self,
        owner: str,
        repo: str,
        id: int,
        attachment_id: int,
    ) -> Attachment:
        """Get a specific attachment on a comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID
            attachment_id: Attachment ID

        Returns:
            The attachment

        Raises:
            GiteaAPIError: If the attachment doesn't exist
        """
        logger.debug(f"Getting attachment {attachment_id} for comment {owner}/{repo}#{id}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/comments/{id}/assets/{attachment_id}")
        return Attachment(response)

    def edit_comment_attachment(
        self,
        owner: str,
        repo: str,
        id: int,
        attachment_id: int,
        name: str,
    ) -> Attachment:
        """Edit an existing attachment on a comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID
            attachment_id: Attachment ID
            name: New attachment name

        Returns:
            The updated attachment

        Raises:
            GiteaAPIError: If the attachment doesn't exist or couldn't be updated
        """
        attachment_data = EditAttachmentOption(name=name)
        
        logger.debug(f"Editing attachment {attachment_id} for comment {owner}/{repo}#{id}")
        response = self.client.patch(
            f"repos/{owner}/{repo}/issues/comments/{id}/assets/{attachment_id}",
            json_data=attachment_data.to_dict(),
        )
        
        return Attachment(response)

    def delete_comment_attachment(
        self,
        owner: str,
        repo: str,
        id: int,
        attachment_id: int,
    ) -> bool:
        """Delete an attachment from a comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID
            attachment_id: Attachment ID

        Returns:
            True if the attachment was deleted successfully

        Raises:
            GiteaAPIError: If the attachment doesn't exist or couldn't be deleted
        """
        logger.debug(f"Deleting attachment {attachment_id} from comment {owner}/{repo}#{id}")
        self.client.delete(f"repos/{owner}/{repo}/issues/comments/{id}/assets/{attachment_id}")
        return True
