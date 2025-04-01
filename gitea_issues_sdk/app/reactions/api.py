"""API client for Gitea reactions."""

import logging
from typing import Dict, List, Optional, Union

from ..client import GiteaClient
from .models import Reaction, EditReactionOption

logger = logging.getLogger("gitea_issues_sdk")


class ReactionsAPI:
    """API client for working with Gitea reactions."""

    def __init__(self, client: GiteaClient):
        """Initialize the reactions API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_issue_reactions(
        self,
        owner: str,
        repo: str,
        index: int,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Reaction]:
        """List reactions on an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            page: Page number
            limit: Page size

        Returns:
            List of reactions on the issue
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing reactions for issue {owner}/{repo}#{index} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}/reactions", params=params)
        
        reactions = []
        for reaction_data in response:
            try:
                reactions.append(Reaction(reaction_data))
            except Exception as e:
                logger.error(f"Error parsing reaction data: {e}")
                
        return reactions

    def add_issue_reaction(
        self,
        owner: str,
        repo: str,
        index: int,
        content: str,
    ) -> Reaction:
        """Add a reaction to an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            content: Reaction content (e.g., "+1", "-1", "laugh", "confused", "heart", "hooray", "eyes", "rocket")

        Returns:
            The created reaction

        Raises:
            GiteaAPIError: If the reaction couldn't be added
        """
        reaction_data = EditReactionOption(content=content)
        
        logger.debug(f"Adding reaction to issue {owner}/{repo}#{index}: {content}")
        response = self.client.post(
            f"repos/{owner}/{repo}/issues/{index}/reactions",
            json_data=reaction_data.to_dict(),
        )
        
        return Reaction(response)

    def remove_issue_reaction(
        self,
        owner: str,
        repo: str,
        index: int,
        content: str,
    ) -> bool:
        """Remove a reaction from an issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            content: Reaction content to remove

        Returns:
            True if the reaction was removed successfully

        Raises:
            GiteaAPIError: If the reaction couldn't be removed
        """
        logger.debug(f"Removing reaction from issue {owner}/{repo}#{index}: {content}")
        self.client.delete(
            f"repos/{owner}/{repo}/issues/{index}/reactions",
            json_data={"content": content},
        )
        return True

    def list_comment_reactions(
        self,
        owner: str,
        repo: str,
        id: int,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Reaction]:
        """List reactions on a comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID
            page: Page number
            limit: Page size

        Returns:
            List of reactions on the comment
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing reactions for comment {owner}/{repo}#{id} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/comments/{id}/reactions", params=params)
        
        reactions = []
        for reaction_data in response:
            try:
                reactions.append(Reaction(reaction_data))
            except Exception as e:
                logger.error(f"Error parsing reaction data: {e}")
                
        return reactions

    def add_comment_reaction(
        self,
        owner: str,
        repo: str,
        id: int,
        content: str,
    ) -> Reaction:
        """Add a reaction to a comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID
            content: Reaction content (e.g., "+1", "-1", "laugh", "confused", "heart", "hooray", "eyes", "rocket")

        Returns:
            The created reaction

        Raises:
            GiteaAPIError: If the reaction couldn't be added
        """
        reaction_data = EditReactionOption(content=content)
        
        logger.debug(f"Adding reaction to comment {owner}/{repo}#{id}: {content}")
        response = self.client.post(
            f"repos/{owner}/{repo}/issues/comments/{id}/reactions",
            json_data=reaction_data.to_dict(),
        )
        
        return Reaction(response)

    def remove_comment_reaction(
        self,
        owner: str,
        repo: str,
        id: int,
        content: str,
    ) -> bool:
        """Remove a reaction from a comment.

        Args:
            owner: Repository owner
            repo: Repository name
            id: Comment ID
            content: Reaction content to remove

        Returns:
            True if the reaction was removed successfully

        Raises:
            GiteaAPIError: If the reaction couldn't be removed
        """
        logger.debug(f"Removing reaction from comment {owner}/{repo}#{id}: {content}")
        self.client.delete(
            f"repos/{owner}/{repo}/issues/comments/{id}/reactions",
            json_data={"content": content},
        )
        return True
