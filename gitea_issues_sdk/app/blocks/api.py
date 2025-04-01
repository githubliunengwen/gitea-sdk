"""API client for Gitea issue blocking relationships."""

import logging
from typing import Dict, List, Optional, Union

from ..client import GiteaClient
from ..issues.models import Issue
from .models import IssueMeta

logger = logging.getLogger("gitea_issues_sdk")


class BlocksAPI:
    """API client for working with Gitea issue blocking relationships."""

    def __init__(self, client: GiteaClient):
        """Initialize the blocks API client.

        Args:
            client: The Gitea API client
        """
        self.client = client

    def list_blocks(
        self,
        owner: str,
        repo: str,
        index: int,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Issue]:
        """List issues that are blocked by this issue.

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            page: Page number
            limit: Page size

        Returns:
            List of issues that are blocked by this issue
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing blocks for issue {owner}/{repo}#{index} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}/blocks", params=params)
        
        issues = []
        for issue_data in response:
            try:
                issues.append(Issue(issue_data))
            except Exception as e:
                logger.error(f"Error parsing issue data: {e}")
                
        return issues

    def create_block(
        self,
        owner: str,
        repo: str,
        index: int,
        blocked_owner: str,
        blocked_repo: str,
        blocked_index: int,
    ) -> Issue:
        """Block an issue with another issue.

        The issue specified by (owner, repo, index) will block the issue specified by
        (blocked_owner, blocked_repo, blocked_index).

        Args:
            owner: Repository owner of the blocking issue
            repo: Repository name of the blocking issue
            index: Issue number of the blocking issue
            blocked_owner: Repository owner of the issue to be blocked
            blocked_repo: Repository name of the issue to be blocked
            blocked_index: Issue number of the issue to be blocked

        Returns:
            The blocked issue

        Raises:
            GiteaAPIError: If the block couldn't be created
        """
        issue_meta = IssueMeta(
            owner=blocked_owner,
            repo=blocked_repo,
            index=blocked_index,
        )
        
        logger.debug(f"Creating block: {owner}/{repo}#{index} blocks {blocked_owner}/{blocked_repo}#{blocked_index}")
        response = self.client.post(
            f"repos/{owner}/{repo}/issues/{index}/blocks",
            json_data=issue_meta.to_dict(),
        )
        
        return Issue(response)

    def remove_block(
        self,
        owner: str,
        repo: str,
        index: int,
        blocked_owner: str,
        blocked_repo: str,
        blocked_index: int,
    ) -> bool:
        """Unblock an issue that is blocked by another issue.

        Args:
            owner: Repository owner of the blocking issue
            repo: Repository name of the blocking issue
            index: Issue number of the blocking issue
            blocked_owner: Repository owner of the issue to be unblocked
            blocked_repo: Repository name of the issue to be unblocked
            blocked_index: Issue number of the issue to be unblocked

        Returns:
            True if the block was removed successfully

        Raises:
            GiteaAPIError: If the block couldn't be removed
        """
        issue_meta = IssueMeta(
            owner=blocked_owner,
            repo=blocked_repo,
            index=blocked_index,
        )
        
        logger.debug(f"Removing block: {owner}/{repo}#{index} unblocks {blocked_owner}/{blocked_repo}#{blocked_index}")
        self.client.delete(
            f"repos/{owner}/{repo}/issues/{index}/blocks",
            json_data=issue_meta.to_dict(),
        )
        return True

    def list_dependencies(
        self,
        owner: str,
        repo: str,
        index: int,
        page: int = 1,
        limit: Optional[int] = None,
    ) -> List[Issue]:
        """List issues that block this issue (dependencies).

        Args:
            owner: Repository owner
            repo: Repository name
            index: Issue number
            page: Page number
            limit: Page size

        Returns:
            List of issues that block this issue
        """
        params: Dict[str, Union[str, int]] = {"page": page}
        
        if limit:
            params["limit"] = limit
            
        logger.debug(f"Listing dependencies for issue {owner}/{repo}#{index} with params: {params}")
        response = self.client.get(f"repos/{owner}/{repo}/issues/{index}/dependencies", params=params)
        
        issues = []
        for issue_data in response:
            try:
                issues.append(Issue(issue_data))
            except Exception as e:
                logger.error(f"Error parsing issue data: {e}")
                
        return issues

    def create_dependency(
        self,
        owner: str,
        repo: str,
        index: int,
        dependency_owner: str,
        dependency_repo: str,
        dependency_index: int,
    ) -> Issue:
        """Add a dependency to an issue.

        The issue specified by (dependency_owner, dependency_repo, dependency_index) will block
        the issue specified by (owner, repo, index).

        Args:
            owner: Repository owner of the dependent issue
            repo: Repository name of the dependent issue
            index: Issue number of the dependent issue
            dependency_owner: Repository owner of the dependency issue
            dependency_repo: Repository name of the dependency issue
            dependency_index: Issue number of the dependency issue

        Returns:
            The dependency issue

        Raises:
            GiteaAPIError: If the dependency couldn't be created
        """
        issue_meta = IssueMeta(
            owner=dependency_owner,
            repo=dependency_repo,
            index=dependency_index,
        )
        
        logger.debug(f"Creating dependency: {dependency_owner}/{dependency_repo}#{dependency_index} blocks {owner}/{repo}#{index}")
        response = self.client.post(
            f"repos/{owner}/{repo}/issues/{index}/dependencies",
            json_data=issue_meta.to_dict(),
        )
        
        return Issue(response)

    def remove_dependency(
        self,
        owner: str,
        repo: str,
        index: int,
        dependency_owner: str,
        dependency_repo: str,
        dependency_index: int,
    ) -> bool:
        """Remove a dependency from an issue.

        Args:
            owner: Repository owner of the dependent issue
            repo: Repository name of the dependent issue
            index: Issue number of the dependent issue
            dependency_owner: Repository owner of the dependency issue
            dependency_repo: Repository name of the dependency issue
            dependency_index: Issue number of the dependency issue

        Returns:
            True if the dependency was removed successfully

        Raises:
            GiteaAPIError: If the dependency couldn't be removed
        """
        issue_meta = IssueMeta(
            owner=dependency_owner,
            repo=dependency_repo,
            index=dependency_index,
        )
        
        logger.debug(f"Removing dependency: {dependency_owner}/{dependency_repo}#{dependency_index} unblocks {owner}/{repo}#{index}")
        self.client.delete(
            f"repos/{owner}/{repo}/issues/{index}/dependencies",
            json_data=issue_meta.to_dict(),
        )
        return True
