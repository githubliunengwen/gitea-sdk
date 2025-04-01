"""API client for Gitea issue comments."""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Union

from ..client import GiteaClient
from .models import Comment, CreateCommentOption, EditCommentOption

logger = logging.getLogger("gitea_issues_sdk")


class CommentsAPI:
    """API client for working with Gitea issue comments."""

    def __init__(self, client: GiteaClient):
        """Initialize the comments API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_repo_comments(
        self,
        owner: str,
        repo: str,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Comment]:
        """List all comments in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            since: Only show comments updated after this time
            before: Only show comments updated before this time
            page: Page number
            limit: Page size

        Returns:
            List of comments in the repository
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if since:
            params["since"] = since.isoformat()
        if before:
            params["before"] = before.isoformat()
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing comments for {owner}/{repo} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/comments", params=params)
        
        comments = []
        for comment_data in response:
            try:
                comments.append(Comment(comment_data))
            except Exception as e:
                logger.error(f"Error parsing comment data: {e}")
                
        return comments

    def get_comment(self, owner: str, repo: str, id: int) -> Comment:
        """Get a specific comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID

        Returns:
            The comment

        Raises:
            GiteaAPIError: If the comment doesn't exist
        """
        logger.debug(f"Getting comment {owner}/{repo}#{id}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/comments/{id}")
        return Comment(response)

    def create_comment(self, owner: str, repo: str, index: int, body: str) -> Comment:
        """Create a new comment on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            body: Comment body

        Returns:
            The created comment

        Raises:
            GiteaAPIError: If the comment couldn't be created
        """
        comment_data = CreateCommentOption(body=body)
        
        logger.debug(f"Creating comment on issue {owner}/{repo}#{index}")
        response = self.client.post(
            f"repos/{owner}/{repo}/issues/{index}/comments",
            json_data=comment_data.to_dict(),
        )
        
        return Comment(response)

    def edit_comment(self, owner: str, repo: str, id: int, body: str) -> Comment:
        """Edit an existing comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID
            body: New comment body

        Returns:
            The updated comment

        Raises:
            GiteaAPIError: If the comment doesn't exist or couldn't be updated
        """
        comment_data = EditCommentOption(body=body)
        
        logger.debug(f"Editing comment {owner}/{repo}#{id}")
        response = self.client.patch(
            f"repos/{owner}/{repo}/issues/comments/{id}",
            json_data=comment_data.to_dict(),
        )
        
        return Comment(response)

    def delete_comment(self, owner: str, repo: str, id: int) -> bool:
        """Delete a comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID

        Returns:
            True if the comment was deleted successfully

        Raises:
            GiteaAPIError: If the comment doesn't exist or couldn't be deleted
        """
        logger.debug(f"Deleting comment {owner}/{repo}#{id}")
        self.client.delete(f"repos/{owner}/{repo}/issues/comments/{id}")
        return True

    def list_issue_comments(
        self,
        owner: str,
        repo: str,
        index: int,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Comment]:
        """List comments on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            since: Only show comments created after this time
            before: Only show comments created before this time
            page: Page number
            limit: Page size

        Returns:
            List of comments on the issue
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if since:
            params["since"] = since.isoformat()
        if before:
            params["before"] = before.isoformat()
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing comments for issue {owner}/{repo}#{index} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}/comments", params=params)
        
        comments = []
        for comment_data in response:
            try:
                comments.append(Comment(comment_data))
            except Exception as e:
                logger.error(f"Error parsing comment data: {e}")
                
        return comments
