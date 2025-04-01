"""API client for Gitea pinned issues."""

import logging
from typing import Dict, List, Optional, Union

from ..client import GiteaClient
from ..issues.models import Issue

logger = logging.getLogger("gitea_issues_sdk")


class PinnedAPI:
    """API client for working with Gitea pinned issues."""

    def __init__(self, client: GiteaClient):
        """Initialize the pinned issues API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_pinned_issues(
        self,
        owner: str,
        repo: str,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Issue]:
        """List pinned issues in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            page: Page number
            limit: Page size

        Returns:
            List of pinned issues in the repository
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing pinned issues for repository {owner}/{repo} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/pinned", params=params)
        
        issues = []
        for issue_data in response:
            try:
                issues.append(Issue(issue_data))
            except Exception as e:
                logger.error(f"Error parsing issue data: {e}")
                
        return issues

    def pin_issue(
        self,
        owner: str,
        repo: str,
        index: int,
    ) -> bool:
        """Pin an issue in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number

        Returns:
            True if the issue was pinned successfully

        Raises:
            GiteaAPIError: If the issue couldn't be pinned
        """
        logger.debug(f"Pinning issue {owner}/{repo}#{index}")
        self.client.post(f"repos/{owner}/{repo}/issues/{index}/pin")
        return True

    def unpin_issue(
        self,
        owner: str,
        repo: str,
        index: int,
    ) -> bool:
        """Unpin an issue in a repository.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number

        Returns:
            True if the issue was unpinned successfully

        Raises:
            GiteaAPIError: If the issue couldn't be unpinned
        """
        logger.debug(f"Unpinning issue {owner}/{repo}#{index}")
        self.client.delete(f"repos/{owner}/{repo}/issues/{index}/pin")
        return True
